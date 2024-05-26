import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CollectionDataService } from '../../services/data/collection-data.service';

@Component({
    selector: 'app-collection',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './collection.component.html',
    styleUrl: './collection.component.css'
})
export class CollectionComponent {

    volumes$ = this.collectionDataService.collectionVolumes$;

    constructor(private collectionDataService: CollectionDataService) {
        this.volumes$.subscribe(volumes => {
            console.log(volumes);
        });
    }

}
