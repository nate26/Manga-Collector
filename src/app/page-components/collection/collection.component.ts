import { Component } from '@angular/core';
import { IManga } from '../../interfaces/iManga.interface';
import { CollectionService } from '../../services/collection.service';
import { CommonModule } from '@angular/common';
import { RouterModule, RouterOutlet } from '@angular/router';

export enum EViewLayout {
    SERIES, TABLE, VOLUME
}

@Component({
    selector: 'app-collection',
    standalone: true,
    imports: [CommonModule, RouterOutlet, RouterModule],
    templateUrl: './collection.component.html',
    styleUrl: './collection.component.css'
})
export class CollectionComponent {

    constructor(private collectionService: CollectionService) {
        collectionService.userId$.next('1234')
    }

    editVolume(vol: (IManga)) {
        console.log(vol)
    }

}
