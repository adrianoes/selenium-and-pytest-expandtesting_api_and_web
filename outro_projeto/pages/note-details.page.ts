import { expect, type Locator, type Page } from '@playwright/test';

export class NoteDetailsPage {
  readonly page: Page;
  readonly noteCard: Locator;
  readonly noteTitle: Locator;
  readonly noteDescription: Locator;
  readonly noteUpdatedAt: Locator;
  readonly toggleSwitch: Locator;
  readonly editButton: Locator;
  readonly deleteButton: Locator;
  readonly confirmDeleteButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.noteCard = page.getByTestId('note-card');
    this.noteTitle = page.getByTestId('note-card-title');
    this.noteDescription = page.getByTestId('note-card-description');
    this.noteUpdatedAt = page.getByTestId('note-card-updated-at');
    this.toggleSwitch = page.getByTestId('toggle-note-switch');
    this.editButton = page.getByTestId('note-edit');
    this.deleteButton = page.getByTestId('note-delete');
    this.confirmDeleteButton = page.getByTestId('note-delete-confirm');
  }

  async expectLoaded(): Promise<void> {
    await expect(this.page).toHaveURL(/\/notes\/app\/notes\/[a-f0-9]{24}/);
    await expect(this.noteCard).toBeVisible();
  }

  async captureNoteIdFromUrl(): Promise<string> {
    const url = this.page.url();
    const parts = url.split('/notes/app/notes/');
    return parts[1] ?? '';
  }

  async openEditModal(): Promise<void> {
    await this.editButton.click();
  }

  async deleteNote(): Promise<void> {
    await this.deleteButton.click();
    await this.confirmDeleteButton.click();
  }
}
