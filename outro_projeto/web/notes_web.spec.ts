import { expect, test } from '@playwright/test';

import { generateInvalidNoteData, generateNoteData } from '../../data/faker';
import { HomePage } from '../../pages/home.page';
import { LoginPage } from '../../pages/login.page';
import { NoteDetailsPage } from '../../pages/note-details.page';
import { NoteModalPage } from '../../pages/note-modal.page';
import {
  blockAdsAndIframes,
  createFixtureKey,
  createNoteViaWeb,
  createUserViaWeb,
  deleteJsonFile,
  deleteUserViaWeb,
  logInUserViaWeb,
  readFixtureData,
} from '../support/web_commands';

const categoryColorMap: Record<string, string> = {
  Home: 'rgb(255, 145, 0)',
  Work: 'rgb(92, 107, 192)',
  Personal: 'rgb(50, 140, 160)',
};

const completedColor = 'rgba(40, 46, 41, 0.6)';

test.describe('Notes Web Tests', () => {
  test.beforeEach(async ({ page }) => {
    await blockAdsAndIframes(page);
  });

  test('TC550 - Create a new note via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    const homePage = new HomePage(page);
    const loginPage = new LoginPage(page);
    const noteDetailsPage = new NoteDetailsPage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await createNoteViaWeb(page, fixtureKey);
    const fixture = readFixtureData(fixtureKey);

    const card = homePage.noteCardByTitle(fixture.note_title);
    await expect(card).toBeVisible();
    await expect(homePage.noteCardTitle(card)).toContainText(fixture.note_title);
    await expect(homePage.noteCardDescription(card)).toContainText(fixture.note_description);

    const listUpdatedAt = (await homePage.noteCardUpdatedAt(card).innerText()).trim();
    expect(listUpdatedAt.length).toBeGreaterThan(10);

    if (fixture.note_completed) {
      await expect(homePage.noteCardToggleSwitch(card)).toBeChecked();
    } else {
      await expect(homePage.noteCardToggleSwitch(card)).not.toBeChecked();
    }

    const headerBackgroundColor = await homePage.noteCardTitle(card).evaluate((el) => getComputedStyle(el).backgroundColor);
    const expectedColor = fixture.note_completed ? completedColor : categoryColorMap[fixture.note_category];
    expect(headerBackgroundColor).toBe(expectedColor);

    await page.goto(`/notes/app/notes/${fixture.note_id}`);
    await noteDetailsPage.expectLoaded();

    await expect(noteDetailsPage.noteTitle).toContainText(fixture.note_title);
    await expect(noteDetailsPage.noteDescription).toContainText(fixture.note_description);

    const detailsUpdatedAt = (await noteDetailsPage.noteUpdatedAt.innerText()).trim();
    expect(detailsUpdatedAt).toBe(listUpdatedAt);

    if (fixture.note_completed) {
      await expect(noteDetailsPage.toggleSwitch).toBeChecked();
    } else {
      await expect(noteDetailsPage.toggleSwitch).not.toBeChecked();
    }

    const detailHeaderColor = await noteDetailsPage.noteTitle.evaluate((el) => getComputedStyle(el).backgroundColor);
    expect(detailHeaderColor).toBe(expectedColor);

    const noteIdFromUrl = await noteDetailsPage.captureNoteIdFromUrl();
    expect(noteIdFromUrl).toBe(fixture.note_id);

    await deleteUserViaWeb(page);
    await loginPage.expectAccountDeletedAlert();
    await deleteJsonFile(fixtureKey);
  });

  test('TC560 - Create a new note via WEB - Invalid title @WEB @FULL @NEGATIVE', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    const homePage = new HomePage(page);
    const loginPage = new LoginPage(page);
    const noteModalPage = new NoteModalPage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await homePage.goto();
    await homePage.clickAddNote();

    const note = generateNoteData();
    const invalidNote = generateInvalidNoteData();
    await noteModalPage.categorySelect.selectOption(note.category);
    await noteModalPage.titleInput.fill(invalidNote.title);
    await noteModalPage.descriptionInput.fill(note.description);
    await noteModalPage.submitButton.click();

    await noteModalPage.expectTitleValidationError();

    await deleteUserViaWeb(page);
    await loginPage.expectAccountDeletedAlert();
    await deleteJsonFile(fixtureKey);
  });

  test('TC570 - Create a new note via WEB - Invalid description @WEB @FULL @NEGATIVE', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    const homePage = new HomePage(page);
    const loginPage = new LoginPage(page);
    const noteModalPage = new NoteModalPage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await homePage.goto();
    await homePage.clickAddNote();

    const note = generateNoteData();
    const invalidNote = generateInvalidNoteData();
    await noteModalPage.categorySelect.selectOption(note.category);
    await noteModalPage.titleInput.fill(note.title);
    await noteModalPage.descriptionInput.fill(invalidNote.description);
    await noteModalPage.submitButton.click();

    await noteModalPage.expectDescriptionValidationError();

    await deleteUserViaWeb(page);
    await loginPage.expectAccountDeletedAlert();
    await deleteJsonFile(fixtureKey);
  });

  test('TC580 - Get all notes via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    const homePage = new HomePage(page);
    const loginPage = new LoginPage(page);
    const noteModalPage = new NoteModalPage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);

    const notes = [generateNoteData(), generateNoteData(), generateNoteData(), generateNoteData()];

    for (const note of notes) {
      await homePage.goto();
      await homePage.clickAddNote();
      await noteModalPage.expectAddModalVisible();
      await noteModalPage.fillAndSubmit(note);

      const createdCard = homePage.noteCardByTitle(note.title);
      await expect(createdCard).toBeVisible();
    }

    await homePage.goto();
    await expect(homePage.noteCards.first()).toBeVisible();
    const noteCount = await homePage.noteCards.count();
    expect(noteCount).toBeGreaterThanOrEqual(4);

    for (const note of notes) {
      const card = homePage.noteCardByTitle(note.title);
      await expect(card).toBeVisible();
      await expect(homePage.noteCardTitle(card)).toContainText(note.title);
      await expect(homePage.noteCardDescription(card)).toContainText(note.description);
    }

    await deleteUserViaWeb(page);
    await loginPage.expectAccountDeletedAlert();
    await deleteJsonFile(fixtureKey);
  });

  test('TC590 - Get note by ID via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    const homePage = new HomePage(page);
    const loginPage = new LoginPage(page);
    const noteDetailsPage = new NoteDetailsPage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await createNoteViaWeb(page, fixtureKey);
    const fixture = readFixtureData(fixtureKey);

    await homePage.clickViewByTitle(fixture.note_title);
    await noteDetailsPage.expectLoaded();
    await expect(noteDetailsPage.noteTitle).toContainText(fixture.note_title);
    await expect(noteDetailsPage.noteDescription).toContainText(fixture.note_description);

    const noteIdFromUrl = await noteDetailsPage.captureNoteIdFromUrl();
    expect(noteIdFromUrl).toBe(fixture.note_id);

    await deleteUserViaWeb(page);
    await loginPage.expectAccountDeletedAlert();
    await deleteJsonFile(fixtureKey);
  });

  test('TC600 - Update note via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    const homePage = new HomePage(page);
    const loginPage = new LoginPage(page);
    const noteDetailsPage = new NoteDetailsPage(page);
    const noteModalPage = new NoteModalPage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await createNoteViaWeb(page, fixtureKey);
    const fixture = readFixtureData(fixtureKey);
    const updatedNote = generateNoteData();

    await homePage.clickViewByTitle(fixture.note_title);
    await noteDetailsPage.expectLoaded();
    await noteDetailsPage.openEditModal();
    await noteModalPage.expectEditModalVisible();

    await noteModalPage.titleInput.fill(updatedNote.title);
    await noteModalPage.descriptionInput.fill(updatedNote.description);
    await noteModalPage.submitButton.click();

    await expect(noteDetailsPage.noteTitle).toContainText(updatedNote.title);
    await expect(noteDetailsPage.noteDescription).toContainText(updatedNote.description);

    await deleteUserViaWeb(page);
    await loginPage.expectAccountDeletedAlert();
    await deleteJsonFile(fixtureKey);
  });

  test('TC610 - Update note via WEB - Invalid title @WEB @FULL @NEGATIVE', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    const homePage = new HomePage(page);
    const loginPage = new LoginPage(page);
    const noteDetailsPage = new NoteDetailsPage(page);
    const noteModalPage = new NoteModalPage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await createNoteViaWeb(page, fixtureKey);
    const fixture = readFixtureData(fixtureKey);
    const invalidNote = generateInvalidNoteData();

    await homePage.clickViewByTitle(fixture.note_title);
    await noteDetailsPage.expectLoaded();
    await noteDetailsPage.openEditModal();
    await noteModalPage.expectEditModalVisible();
    await noteModalPage.titleInput.fill(invalidNote.title);
    await noteModalPage.submitButton.click();

    await noteModalPage.expectTitleValidationError();

    await deleteUserViaWeb(page);
    await loginPage.expectAccountDeletedAlert();
    await deleteJsonFile(fixtureKey);
  });

  test('TC620 - Toggle note completed status via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    const homePage = new HomePage(page);
    const loginPage = new LoginPage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await createNoteViaWeb(page, fixtureKey);
    const fixture = readFixtureData(fixtureKey);

    const card = homePage.noteCardByTitle(fixture.note_title);
    const toggleSwitch = homePage.noteCardToggleSwitch(card);

    await toggleSwitch.click();

    if (fixture.note_completed) {
      await expect(toggleSwitch).not.toBeChecked();
    } else {
      await expect(toggleSwitch).toBeChecked();
    }

    await deleteUserViaWeb(page);
    await loginPage.expectAccountDeletedAlert();
    await deleteJsonFile(fixtureKey);
  });

  test('TC630 - Delete note via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    const homePage = new HomePage(page);
    const loginPage = new LoginPage(page);
    const noteDetailsPage = new NoteDetailsPage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await createNoteViaWeb(page, fixtureKey);
    const fixture = readFixtureData(fixtureKey);

    await homePage.clickViewByTitle(fixture.note_title);
    await noteDetailsPage.expectLoaded();

    await noteDetailsPage.deleteNote();

    await homePage.expectNotesListVisible();
    await homePage.expectEmptyNotesMessage();

    await deleteUserViaWeb(page);
    await loginPage.expectAccountDeletedAlert();
    await deleteJsonFile(fixtureKey);
  });
});
