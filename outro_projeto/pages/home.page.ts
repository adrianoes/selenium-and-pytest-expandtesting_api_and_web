import { expect, type Locator, type Page } from '@playwright/test';

export class HomePage {
  readonly page: Page;
  readonly welcomeTitle: Locator;
  readonly createAccountButton: Locator;
  readonly addNoteButton: Locator;
  readonly notesList: Locator;
  readonly noteCards: Locator;
  readonly emptyNotesMessage: Locator;
  readonly profileButton: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.welcomeTitle = page.getByRole('heading', { name: 'Welcome to Notes App' });
    this.createAccountButton = page.getByTestId('open-register-view');
    this.addNoteButton = page.getByTestId('add-new-note');
    this.notesList = page.getByTestId('notes-list');
    this.noteCards = page.getByTestId('note-card');
    this.emptyNotesMessage = page.getByText(/You don't have any notes|don't have any notes/i);
    this.profileButton = page.getByTestId('profile');
    this.logoutButton = page.getByTestId('logout');
  }

  async goto(): Promise<void> {
    await this.page.goto('/notes/app');
  }

  async expectWelcomeVisible(): Promise<void> {
    await expect(this.welcomeTitle).toBeVisible();
  }

  async clickCreateAccount(): Promise<void> {
    await this.createAccountButton.click();
  }

  async clickAddNote(): Promise<void> {
    await this.addNoteButton.click();
  }

  async expectNotesListVisible(): Promise<void> {
    await expect(this.notesList).toBeVisible();
  }

  noteCardByTitle(title: string): Locator {
    return this.noteCards.filter({ has: this.page.getByTestId('note-card-title').filter({ hasText: title }) }).first();
  }

  noteCardTitle(card: Locator): Locator {
    return card.getByTestId('note-card-title');
  }

  noteCardDescription(card: Locator): Locator {
    return card.getByTestId('note-card-description');
  }

  noteCardUpdatedAt(card: Locator): Locator {
    return card.getByTestId('note-card-updated-at');
  }

  noteCardToggleSwitch(card: Locator): Locator {
    return card.getByTestId('toggle-note-switch');
  }

  async clickViewByTitle(title: string): Promise<void> {
    await this.noteCardByTitle(title).getByTestId('note-view').click();
  }

  async expectLoggedAreaVisible(): Promise<void> {
    await expect(this.profileButton).toBeVisible();
    await expect(this.logoutButton).toBeVisible();
  }

  async expectAddNoteVisible(): Promise<void> {
    await expect(this.addNoteButton).toBeVisible();
  }

  async expectEmptyNotesMessage(): Promise<void> {
    await expect(this.emptyNotesMessage).toBeVisible();
  }

  async logout(): Promise<void> {
    await this.logoutButton.click();
  }

  async goToProfile(): Promise<void> {
    await this.profileButton.click();

    if (!this.page.url().includes('/notes/app/profile')) {
      await this.page.goto('/notes/app/profile');
    }
  }
}
