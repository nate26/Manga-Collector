import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { CollectionComponent } from './page-components/collection/collection.component';
import { RouterOutlet } from '@angular/router';
import { SearchVolumesComponent } from './common/search-volumes/search-volumes.component';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, RouterOutlet, CollectionComponent, SearchVolumesComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})
export class AppComponent {
    title = 'Manga Tracker';

}
