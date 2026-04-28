import { expect, test } from '@playwright/test';
import { generateInvalidPhone, generatePassword, generateUserData, generateUserProfileUpdateData } from '../../data/faker';
import { HomePage } from '../../pages/home.page';
import { RegisterPage } from '../../pages/register.page';
import { LoginPage } from '../../pages/login.page';
import { ProfilePage } from '../../pages/profile.page';
import {
  blockAdsAndIframes,
  createFixtureKey,
  createUserViaWeb,
  deleteJsonFile,
  deleteUserViaWeb,
  logInUserViaWeb,
  readFixtureData,
} from '../support/web_commands';

test.describe('Users Web Tests', () => {
  test.beforeEach(async ({ page }) => {
    await blockAdsAndIframes(page);
  });

  test('TC400 - Successful User Registration via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });

  test('TC410 - Successful Login via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    const homePage = new HomePage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await homePage.goto();
    await homePage.expectLoggedAreaVisible();
    await homePage.expectAddNoteVisible();
    await homePage.expectEmptyNotesMessage();

    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });

  test('TC420 - Profile Data Validation via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    const profilePage = new ProfilePage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    const fixture = readFixtureData(fixtureKey);

    await profilePage.goto();
    await profilePage.expectLoaded();
    await profilePage.expectUserId(fixture.user_id);
    await profilePage.expectUserData(fixture.user_email, fixture.user_name);

    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });

  test('TC430 - User Deletion via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });

  test('TC440 - Create a new user account via WEB - Invalid email @WEB @FULL @NEGATIVE', async ({ page }) => {
    const user = generateUserData();
    const registerPage = new RegisterPage(page);

    await registerPage.goto();
    await registerPage.fillFormWithConfirmPassword(
      {
        ...user,
        user_email: '@' + user.user_email,
      },
      user.user_password,
    );
    await registerPage.submit();
    await registerPage.expectAlertMessage('A valid email address is required');
  });

  test("TC450 - Create a new user account via WEB - Wrong password @WEB @FULL @NEGATIVE", async ({ page }) => {
    const user = generateUserData();
    const registerPage = new RegisterPage(page);

    await registerPage.goto();
    await registerPage.fillFormWithConfirmPassword(user, 'e' + user.user_password);
    await registerPage.submit();

    const mismatchError = page.getByText("Passwords don't match!").or(page.locator('.mb-3 > .invalid-feedback')).first();
    await expect(mismatchError).toBeVisible();
    await expect(mismatchError).toContainText("Passwords don't match!");
  });

  test('TC460 - Log in as an existing user via WEB - Invalid email @WEB @FULL @NEGATIVE', async ({ page }) => {
    const fixtureKey = createFixtureKey();
    const loginPage = new LoginPage(page);

    await createUserViaWeb(page, fixtureKey);
    const fixture = readFixtureData(fixtureKey);

    await loginPage.goto();
    await loginPage.login('e' + fixture.user_email, fixture.user_password);
    await loginPage.expectInvalidCredentialsAlert();

    await logInUserViaWeb(page, fixtureKey);
    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });

  test('TC470 - Log in as an existing user via WEB - Wrong password @WEB @FULL @NEGATIVE', async ({ page }) => {
    const fixtureKey = createFixtureKey();
    const loginPage = new LoginPage(page);

    await createUserViaWeb(page, fixtureKey);
    const fixture = readFixtureData(fixtureKey);

    await loginPage.goto();
    await loginPage.login(fixture.user_email, 'e' + fixture.user_password);
    await loginPage.expectInvalidCredentialsAlert();

    await logInUserViaWeb(page, fixtureKey);
    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });

  test('TC480 - Retrieve user profile information via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();
    const profilePage = new ProfilePage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await profilePage.goto();
    await profilePage.expectLoaded();

    const fixture = readFixtureData(fixtureKey);
    await profilePage.expectUserId(fixture.user_id);
    await profilePage.expectUserData(fixture.user_email, fixture.user_name);

    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });

  test('TC490 - Update user profile information via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();
    const profilePage = new ProfilePage(page);
    const profileUpdate = generateUserProfileUpdateData();

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await profilePage.goto();
    await profilePage.updateProfile(profileUpdate.phone, profileUpdate.company);
    await profilePage.expectProfileUpdated();

    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });

  test('TC500 - Update user profile information via WEB - Invalid company name @WEB @FULL @NEGATIVE', async ({ page }) => {
    const fixtureKey = createFixtureKey();
    const profilePage = new ProfilePage(page);
    const profileUpdate = generateUserProfileUpdateData();

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await profilePage.goto();
    await profilePage.updateProfile(profileUpdate.phone, 'e');
    await profilePage.expectCompanyValidationError();

    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });

  test('TC510 - Update user profile information via WEB - Invalid phone number @WEB @FULL @NEGATIVE', async ({ page }) => {
    const fixtureKey = createFixtureKey();
    const profilePage = new ProfilePage(page);
    const profileUpdate = generateUserProfileUpdateData();

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await profilePage.goto();
    await profilePage.updateProfile(generateInvalidPhone(), profileUpdate.company);
    await profilePage.expectPhoneValidationError();

    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });

  test("TC520 - Change a user's password via WEB @WEB @BASIC @FULL", async ({ page }) => {
    const fixtureKey = createFixtureKey();
    const profilePage = new ProfilePage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    const fixture = readFixtureData(fixtureKey);
    const newPassword = generatePassword();

    await profilePage.goto();
    await profilePage.openChangePassword();
    await profilePage.changePassword(fixture.user_password, newPassword, newPassword);
    await profilePage.expectPasswordUpdated();

    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });

  test("TC530 - Change a user's password via WEB - Wrong password @WEB @FULL @NEGATIVE", async ({ page }) => {
    const fixtureKey = createFixtureKey();
    const profilePage = new ProfilePage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    const fixture = readFixtureData(fixtureKey);
    const newPassword = generatePassword();

    await profilePage.goto();
    await profilePage.openChangePassword();
    await profilePage.changePassword('e' + fixture.user_password, newPassword, newPassword);
    await profilePage.expectCurrentPasswordIncorrect();

    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });

  test('TC540 - Log out a user via WEB @WEB @BASIC @FULL', async ({ page }) => {
    const fixtureKey = createFixtureKey();
    const homePage = new HomePage(page);
    const loginPage = new LoginPage(page);

    await createUserViaWeb(page, fixtureKey);
    await logInUserViaWeb(page, fixtureKey);
    await homePage.goto();
    await homePage.logout();
    await loginPage.expectLoginLinkVisible();

    await logInUserViaWeb(page, fixtureKey);
    await deleteUserViaWeb(page);
    await deleteJsonFile(fixtureKey);
  });
});
