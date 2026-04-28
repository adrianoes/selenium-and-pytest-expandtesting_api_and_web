import { expect, type Locator, type Page } from '@playwright/test';

export type NoteInput = {
  title: string;
  description: string;
  category: 'Home' | 'Work' | 'Personal';
  completed: number;
};

export class NoteModalPage {
  readonly page: Page;
  readonly addModalTitle: Locator;
  readonly editModalTitle: Locator;
  readonly categorySelect: Locator;
  readonly completedCheckbox: Locator;
  readonly titleInput: Locator;
  readonly descriptionInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.addModalTitle = page.getByText('Add new note');
    this.editModalTitle = page.getByText('Edit note');
    this.categorySelect = page.getByTestId('note-category');
    this.completedCheckbox = page.getByTestId('note-completed');
    this.titleInput = page.getByTestId('note-title');
    this.descriptionInput = page.getByTestId('note-description');
    this.submitButton = page.getByTestId('note-submit');
  }

  async expectAddModalVisible(): Promise<void> {
    await expect(this.addModalTitle).toBeVisible();
    await expect(this.categorySelect).toBeVisible();
  }

  async expectEditModalVisible(): Promise<void> {
    await expect(this.editModalTitle).toBeVisible();
    await expect(this.categorySelect).toBeVisible();
  }

  async fillAndSubmit(note: NoteInput): Promise<boolean> {
    await this.categorySelect.selectOption(note.category);

    for (let i = 0; i < note.completed; i++) {
      await this.completedCheckbox.click();
    }

    await this.titleInput.fill(note.title);
    await this.descriptionInput.fill(note.description);

    const expectedCompleted = note.completed % 2 !== 0;
    await this.submitButton.click();
    return expectedCompleted;
  }

  async expectTitleValidationError(): Promise<void> {
    await expect(this.page.getByText('Title should be between 4 and 100 characters')).toBeVisible();
  }

  async expectDescriptionValidationError(): Promise<void> {
    await expect(this.page.getByText('Description should be between 4 and 1000 characters')).toBeVisible();
  }
}
