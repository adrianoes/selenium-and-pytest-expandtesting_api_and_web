import { expect, type Locator, type Page } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly loginTitle: Locator;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginSubmitButton: Locator;
  readonly accountDeletedMessage: Locator;
  readonly loginLink: Locator;

  constructor(page: Page) {
    this.page = page;
    this.loginTitle = page.getByRole('heading', { name: 'Login' });
    this.emailInput = page.getByTestId('login-email');
    this.passwordInput = page.getByTestId('login-password');
    this.loginSubmitButton = page.getByTestId('login-submit');
    this.accountDeletedMessage = page.getByTestId('alert-message');
    this.loginLink = page.getByRole('link', { name: 'Login' }).or(page.locator('[href="/notes/app/login"]')).first();
  }

  async goto(): Promise<void> {
    await this.page.goto('/notes/app/login');
  }

  async expectLoaded(): Promise<void> {
    await expect(this.page).toHaveURL(/\/notes\/app\/login/);
    await expect(this.loginTitle).toBeVisible();
  }

  async login(email: string, password: string): Promise<void> {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginSubmitButton.click();
  }

  async expectAccountDeletedAlert(): Promise<void> {
    await expect(this.page).toHaveURL(/\/notes\/app\/login/);
    await expect(this.accountDeletedMessage).toBeVisible();
    await expect(this.accountDeletedMessage).toContainText('Your account has been deleted. You should create a new account to continue.');
  }

  async expectInvalidCredentialsAlert(): Promise<void> {
    await expect(this.accountDeletedMessage).toBeVisible();
    await expect(this.accountDeletedMessage).toContainText('Incorrect email address or password');
  }

  async expectLoginLinkVisible(): Promise<void> {
    await expect(this.loginLink).toBeVisible();
    await expect(this.loginLink).toContainText('Login');
  }
}
