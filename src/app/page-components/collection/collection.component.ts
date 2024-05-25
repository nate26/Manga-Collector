import { Component } from '@angular/core';
import { CollectionService } from '../../services/collection.service';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-collection',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './collection.component.html',
    styleUrl: './collection.component.css'
})
export class CollectionComponent {

    constructor(private collectionService: CollectionService) {
        // collectionService.userId.set('1234')
    }

}
