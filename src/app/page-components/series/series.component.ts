import { Component, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { SeriesDataService } from '../../services/data/series-data.service';
import { IVolume } from '../../interfaces/iVolume.interface';
import { NgStyle } from '@angular/common';

@Component({
    selector: 'app-series',
    standalone: true,
    imports: [NgStyle],
    templateUrl: './series.component.html',
    styleUrl: './series.component.css'
})
export class SeriesComponent {

    seriesDataService = inject(SeriesDataService);

    series = toSignal(this.seriesDataService.collectionSeries$, { initialValue: [] });

    getVolumeStatusColor(volume: IVolume) {
        if (volume.user_collection_data.length > 0) {
            return { 'background-color': '#A6F7CD' }; //CDA6F7
        }
        if (!volume.release_date) {
            return { 'background-color': '#C4C4C4' };
        }
        const today = new Date();
        const releaseDate = new Date(volume.release_date);
        if (releaseDate.getTime() > today.getTime()) {
            return { 'background-color': '#F7CDA6' };
        }
        else {
            return { 'background-color': '#EBEBEB' };
        }
    }

    navTo(url: string) {
        window.open(url, '_blank');
    }

}
