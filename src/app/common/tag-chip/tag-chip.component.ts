import { Component, input, output } from '@angular/core';

@Component({
    selector: 'app-tag-chip',
    standalone: true,
    imports: [],
    templateUrl: './tag-chip.component.html',
    styleUrl: './tag-chip.component.css'
})
export class TagChipComponent {

    tagName = input.required<string>();
    editMode = input(false);
    removeTag = output<void>();

    color = '#004741';

}
