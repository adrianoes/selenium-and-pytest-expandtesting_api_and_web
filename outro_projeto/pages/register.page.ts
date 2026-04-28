import { expect, type Locator, type Page } from '@playwright/test';

export type RegisterUserData = {
  user_name: string;
  user_email: string;
  user_password: string;
};

export class RegisterPage {
  readonly page: Page;
  readonly tipText: Locator;
  readonly emailInput: Locator;
  readonly nameInput: Locator;
  readonly passwordInput: Locator;
  readonly confirmPasswordInput: Locator;
  readonly registerSubmitButton: Locator;
  readonly successMessage: Locator;
  readonly alertMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.tipText = page.getByText('Using a valid email address is highly recommended. This will enable you to reset your password if you forget it.');
    this.emailInput = page.getByTestId('register-email');
    this.nameInput = page.getByTestId('register-name');
    this.passwordInput = page.getByTestId('register-password');
    this.confirmPasswordInput = page.getByTestId('register-confirm-password');
    this.registerSubmitButton = page.getByTestId('register-submit');
    this.successMessage = page.getByText('User account created successfully');
    this.alertMessage = page.getByTestId('alert-message');
  }

  async goto(): Promise<void> {
    await this.page.goto('/notes/app/register');
  }

  async expectLoaded(): Promise<void> {
    await expect(this.page).toHaveURL(/\/notes\/app\/register/);
    await expect(this.tipText).toBeVisible();
  }

  async fillForm(user: RegisterUserData): Promise<void> {
    await this.emailInput.fill(user.user_email);
    await this.nameInput.fill(user.user_name);
    await this.passwordInput.fill(user.user_password);
    await this.confirmPasswordInput.fill(user.user_password);
  }

  async submit(): Promise<void> {
    await this.registerSubmitButton.click();
  }

  async fillFormWithConfirmPassword(user: RegisterUserData, confirmPassword: string): Promise<void> {
    await this.emailInput.fill(user.user_email);
    await this.nameInput.fill(user.user_name);
    await this.passwordInput.fill(user.user_password);
    await this.confirmPasswordInput.fill(confirmPassword);
  }

  async expectSuccess(): Promise<void> {
    await expect(this.page).toHaveURL(/\/notes\/app\/register/);
    await expect(this.successMessage).toBeVisible();
  }

  async expectAlertMessage(message: string): Promise<void> {
    await expect(this.alertMessage).toBeVisible();
    await expect(this.alertMessage).toContainText(message);
  }
}
