import { Component, input, output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TagChipComponent } from '../tag-chip/tag-chip.component';

@Component({
  selector: 'app-tag-list',
  imports: [FormsModule, TagChipComponent],
  templateUrl: './tag-list.component.html',
  styleUrl: './tag-list.component.css'
})
export class TagListComponent {
  filterTags = input.required<string[]>();
  editMode = input(false);
  updateTags = output<string[]>();

  filterTagText = '';

  addFilterTag(event: Event) {
    this.filterTagText = '';
    const tagToAdd = (event.target as HTMLInputElement).value.trim();
    if (!tagToAdd || this.filterTags().includes(tagToAdd)) return;

    this.updateTags.emit([...this.filterTags(), tagToAdd]);
  }

  removeFilterTag(tagToRemove: string) {
    this.updateTags.emit(this.filterTags().filter(tag => tag !== tagToRemove));
  }
}
