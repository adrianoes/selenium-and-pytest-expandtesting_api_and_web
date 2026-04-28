import { type Page } from '@playwright/test';
import { faker } from '@faker-js/faker';
declare const require: any;
import fs from 'fs'

import { generateNoteData, generateUserData } from '../../data/faker';
import { HomePage } from '../../pages/home.page';
import { LoginPage } from '../../pages/login.page';
import { NoteModalPage } from '../../pages/note-modal.page';
import { ProfilePage } from '../../pages/profile.page';
import { RegisterPage } from '../../pages/register.page';

const FIXTURE_DIR = 'tests/fixtures';
const fixturePath = (key: string) => `${FIXTURE_DIR}/testdata-${key}.json`;

const readFixture = (key: string): Record<string, any> => JSON.parse(fs.readFileSync(fixturePath(key), 'utf8'));
const writeFixture = (key: string, data: Record<string, any>) => {
  fs.writeFileSync(fixturePath(key), JSON.stringify(data), 'utf8');
};

export const createFixtureKey = (): string => faker.finance.creditCardNumber();

export const saveFixtureData = (key: string, data: Record<string, any>) => {
  writeFixture(key, data);
};

export const readFixtureData = (key: string): Record<string, any> => {
  return readFixture(key);
};

export const updateFixtureData = (key: string, data: Record<string, any>) => {
  const current = readFixture(key);
  writeFixture(key, {
    ...current,
    ...data,
  });
};

export async function blockAdsAndIframes(page: Page): Promise<void> {
  await page.route('**/*', async (route) => {
    const requestUrl = route.request().url();

    // Keep first-party traffic only to avoid ad providers hijacking interactions.
    if (requestUrl.startsWith('data:') || requestUrl.startsWith('blob:') || requestUrl.startsWith('about:')) {
      await route.continue();
      return;
    }

    const hostname = new URL(requestUrl).hostname;
    const isFirstParty = hostname === 'practice.expandtesting.com' || hostname.endsWith('.expandtesting.com');

    if (!isFirstParty) {
      await route.abort();
      return;
    }

    await route.continue();
  });

  await page.addInitScript(() => {
    const clearGoogleVignetteHash = () => {
      if (window.location.hash.includes('google_vignette')) {
        history.replaceState(null, '', `${window.location.pathname}${window.location.search}`);
      }
    };

    const hideIframes = () => {
      for (const iframe of document.querySelectorAll('iframe')) {
        iframe.style.display = 'none';
        iframe.setAttribute('aria-hidden', 'true');
      }
    };

    clearGoogleVignetteHash();
    hideIframes();

    const observer = new MutationObserver(() => {
      clearGoogleVignetteHash();
      hideIframes();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
    window.addEventListener('hashchange', clearGoogleVignetteHash);
  });
}

export async function getFulfilledUserRegisterResponse(page: Page) {
  return page.waitForResponse((response) =>
    response.url().includes('/notes/api/users/register') && response.request().method() === 'POST',
  );
}

export async function getFulfilledNoteCreateResponse(page: Page) {
  return page.waitForResponse((response) =>
    response.url().includes('/notes/api/notes') && response.request().method() === 'POST',
  );
}

export async function createUserViaWeb(page: Page, fixtureKey: string): Promise<void> {
  const user = generateUserData();

  const registerPage = new RegisterPage(page);
  await registerPage.goto();
  await registerPage.expectLoaded();
  await registerPage.fillForm(user);

  const registerResponsePromise = getFulfilledUserRegisterResponse(page);
  await registerPage.submit();
  const registerResponse = await registerResponsePromise;
  const registerBody = await registerResponse.json();

  await registerPage.expectSuccess();

  saveFixtureData(fixtureKey, {
    user_email: user.user_email,
    user_id: registerBody.data.id,
    user_name: user.user_name,
    user_password: user.user_password,
  });
}

export async function logInUserViaWeb(page: Page, fixtureKey: string): Promise<void> {
  const fixture = readFixtureData(fixtureKey);

  const homePage = new HomePage(page);
  const loginPage = new LoginPage(page);
  const profilePage = new ProfilePage(page);

  await loginPage.goto();
  await loginPage.expectLoaded();
  await loginPage.login(fixture.user_email, fixture.user_password);

  await homePage.expectLoggedAreaVisible();
  await profilePage.goto();
  await profilePage.expectLoaded();
  await profilePage.expectUserId(fixture.user_id);
  await profilePage.expectUserData(fixture.user_email, fixture.user_name);
}

export async function deleteUserViaWeb(page: Page): Promise<void> {
  const profilePage = new ProfilePage(page);
  const loginPage = new LoginPage(page);

  await profilePage.goto();
  await profilePage.deleteAccount();
  await loginPage.expectAccountDeletedAlert();
}

export async function createNoteViaWeb(page: Page, fixtureKey: string): Promise<void> {
  const note = generateNoteData();
  const homePage = new HomePage(page);
  const noteModalPage = new NoteModalPage(page);

  let authTokenFromApiRequest: string | undefined;
  const captureApiToken = (request: any) => {
    if (request.url().includes('/notes/api/')) {
      const token = request.headers()['x-auth-token'];
      if (token) {
        authTokenFromApiRequest = token;
      }
    }
  };

  page.on('request', captureApiToken);

  await homePage.goto();
  await homePage.clickAddNote();
  await noteModalPage.expectAddModalVisible();

  await noteModalPage.categorySelect.selectOption(note.category);
  for (let i = 0; i < note.completed; i++) {
    await noteModalPage.completedCheckbox.click();
  }
  await noteModalPage.titleInput.fill(note.title);
  await noteModalPage.descriptionInput.fill(note.description);

  const notesListResponsePromise = page.waitForResponse((response) =>
    response.url().includes('/notes/api/notes') && response.request().method() === 'GET' && response.status() === 200,
  );

  await noteModalPage.submitButton.click();

  let notesListBody: Record<string, any>;
  try {
    const notesListResponse = await notesListResponsePromise;
    notesListBody = (await notesListResponse.json()) as Record<string, any>;
  } catch (error) {
    if (!authTokenFromApiRequest) {
      throw error;
    }

    const notesListApiResponse = await page.request.get('/notes/api/notes', {
      headers: {
        'X-Auth-Token': authTokenFromApiRequest,
      },
    });

    if (!notesListApiResponse.ok()) {
      throw new Error(`Failed to fetch notes list after creation. Status ${notesListApiResponse.status()}`);
    }

    notesListBody = (await notesListApiResponse.json()) as Record<string, any>;
  } finally {
    page.off('request', captureApiToken);
  }

  const createdNote = Array.isArray(notesListBody?.data)
    ? notesListBody.data.find(
        (item: any) =>
          item?.title === note.title &&
          item?.description === note.description &&
          item?.category === note.category,
      )
    : undefined;
  const noteId = createdNote?.id as string | undefined;

  if (!noteId) {
    throw new Error('Could not capture note id from notes list response body after creation');
  }

  const isCompleted = note.completed % 2 !== 0;

  const fixture = readFixture(fixtureKey);
  saveFixtureData(fixtureKey, {
    ...fixture,
    note_id: noteId,
    note_title: note.title,
    note_description: note.description,
    note_category: note.category,
    note_completed: isCompleted,
  });
}

export async function deleteJsonFile(key: string) {
  try {
    fs.unlinkSync(fixturePath(key));
  } catch {
    // ignore cleanup failure if file does not exist
  }
}
