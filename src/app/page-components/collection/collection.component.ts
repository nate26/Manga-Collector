import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { IManga } from '../../interfaces/iManga.interface';
import { ISeriesEditionParsed } from '../../interfaces/iSeries.interface';
import { CollectionService } from '../../services/collection.service';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

export enum EViewLayout {
    SERIES, TABLE, VOLUME
}

@Component({
    selector: 'app-collection',
    standalone: true,
    imports: [CommonModule, RouterOutlet],
    templateUrl: './collection.component.html',
    styleUrl: './collection.component.css'
})
export class CollectionComponent implements OnInit {

    userId = ''; //TODO CHANGE

    series$!: Observable<ISeriesEditionParsed[]>;
    volumes$!: Observable<IManga[]>;

    viewLayout: EViewLayout = EViewLayout.SERIES;

    constructor(private collectionService: CollectionService) { }

    ngOnInit(): void {
        this.volumes$ = this.collectionService.getCollectionAsVolume(this.userId);
        this.series$ = this.collectionService.getCollectionAsSeries(this.userId);
    }

    editVolume(vol: (IManga)) {
        console.log(vol)
    }

    setView(layout: EViewLayout) {
        this.viewLayout = layout;
    }

}
