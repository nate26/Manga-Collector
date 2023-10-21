import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { CollectionService } from 'src/app/services/collection.service';
import { IManga } from 'src/app/interfaces/iManga.interface';
import { ISeriesEditionParsed } from 'src/app/interfaces/iSeries.interface';

export enum EViewLayout {
    SERIES, TABLE, VOLUME
}

@Component({
    selector: 'app-collection',
    templateUrl: './collection.component.html',
    styleUrls: ['./collection.component.css']
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
