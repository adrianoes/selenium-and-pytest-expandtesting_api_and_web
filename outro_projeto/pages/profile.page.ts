import { expect, type Locator, type Page } from '@playwright/test';

export class ProfilePage {
  readonly page: Page;
  readonly profileSettingsTitle: Locator;
  readonly userIdInput: Locator;
  readonly userEmailInput: Locator;
  readonly userNameInput: Locator;
  readonly phoneInput: Locator;
  readonly companyInput: Locator;
  readonly updateProfileButton: Locator;
  readonly changePasswordButton: Locator;
  readonly currentPasswordInput: Locator;
  readonly newPasswordInput: Locator;
  readonly confirmPasswordInput: Locator;
  readonly updatePasswordButton: Locator;
  readonly alertMessage: Locator;
  readonly deleteAccountButton: Locator;
  readonly confirmDeleteButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.profileSettingsTitle = page.getByRole('heading', { name: 'Profile settings' });
    this.userIdInput = page.getByTestId('user-id');
    this.userEmailInput = page.getByTestId('user-email');
    this.userNameInput = page.getByTestId('user-name');
    this.phoneInput = page.getByLabel('Phone').or(page.locator('input[name="phone"]')).first();
    this.companyInput = page.getByLabel('Company').or(page.locator('input[name="company"]')).first();
    this.updateProfileButton = page.getByRole('button', { name: 'Update profile' });
    this.changePasswordButton = page.getByRole('button', { name: 'Change password' });
    this.currentPasswordInput = page.getByTestId('current-password');
    this.newPasswordInput = page.getByTestId('new-password');
    this.confirmPasswordInput = page.getByTestId('confirm-password');
    this.updatePasswordButton = page.getByRole('button', { name: 'Update password' });
    this.alertMessage = page.getByTestId('alert-message');
    this.deleteAccountButton = page.getByTestId('delete-account');
    this.confirmDeleteButton = page.getByTestId('note-delete-confirm');
  }

  async goto(): Promise<void> {
    await this.page.goto('/notes/app/profile');
  }

  async expectLoaded(): Promise<void> {
    await expect(this.page).toHaveURL(/\/notes\/app\/profile(?:#.*)?$/);
    await expect(this.profileSettingsTitle).toBeVisible();
  }

  async expectUserData(email: string, fullName: string): Promise<void> {
    await expect(this.userEmailInput).toHaveValue(email);
    await expect(this.userNameInput).toHaveValue(fullName);
  }

  async expectUserId(userId: string): Promise<void> {
    await expect(this.userIdInput).toHaveValue(userId);
  }

  async updateProfile(phone: string, company: string): Promise<void> {
    await this.phoneInput.fill(phone);
    await this.companyInput.fill(company);
    await this.updateProfileButton.click();
  }

  async expectProfileUpdated(): Promise<void> {
    await expect(this.alertMessage).toBeVisible();
    await expect(this.alertMessage).toContainText('Profile updated successful');
  }

  async expectCompanyValidationError(): Promise<void> {
    const error = this.page.getByText('company name should be between 4 and 30 characters').or(this.page.locator('.mb-4 > .invalid-feedback')).first();
    await expect(error).toBeVisible();
    await expect(error).toContainText('company name should be between 4 and 30 characters');
  }

  async expectPhoneValidationError(): Promise<void> {
    const error = this.page.getByText('Phone number should be between 8 and 20 digits').or(this.page.locator(':nth-child(2) > .mb-2 > .invalid-feedback')).first();
    await expect(error).toBeVisible();
    await expect(error).toContainText('Phone number should be between 8 and 20 digits');
  }

  async openChangePassword(): Promise<void> {
    await this.changePasswordButton.click();
  }

  async changePassword(currentPassword: string, newPassword: string, confirmPassword: string): Promise<void> {
    await this.currentPasswordInput.fill(currentPassword);
    await this.newPasswordInput.fill(newPassword);
    await this.confirmPasswordInput.fill(confirmPassword);
    await this.updatePasswordButton.click();
  }

  async expectPasswordUpdated(): Promise<void> {
    await expect(this.alertMessage).toBeVisible();
    await expect(this.alertMessage).toContainText('The password was successfully updated');
  }

  async expectCurrentPasswordIncorrect(): Promise<void> {
    await expect(this.alertMessage).toBeVisible();
    await expect(this.alertMessage).toContainText('The current password is incorrect');
  }

  async deleteAccount(): Promise<void> {
    await this.deleteAccountButton.click();
    await this.confirmDeleteButton.click();
  }
}
