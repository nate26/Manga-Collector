import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { CollectionComponent } from './page-components/collection/collection.component';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, CollectionComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})
export class AppComponent {
    title = 'Manga Tracker';
}
