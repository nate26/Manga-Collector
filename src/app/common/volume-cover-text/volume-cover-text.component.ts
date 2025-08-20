import { Component, input } from '@angular/core';

@Component({
    selector: 'app-volume-cover-text',
    standalone: true,
    imports: [],
    templateUrl: './volume-cover-text.component.html',
    styleUrl: './volume-cover-text.component.css'
})
export class VolumeCoverTextComponent {

    title = input.required<string>();

}
