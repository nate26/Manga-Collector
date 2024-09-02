import { Component, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { SeriesDataService } from '../../services/data/series-data.service';
import { IVolume } from '../../interfaces/iVolume.interface';
import { NgClass, NgStyle } from '@angular/common';
import { ISeriesRecord } from '../../interfaces/iSeries.interface';
import { LazyImageDirective } from '../../common/directives/lazy-image/lazy-image.directive';
import { VolumeCoverTextComponent } from '../../common/volume-cover-text/volume-cover-text.component';

@Component({
    selector: 'app-series',
    standalone: true,
    imports: [NgStyle, NgClass, LazyImageDirective, VolumeCoverTextComponent],
    templateUrl: './series.component.html',
    styleUrl: './series.component.css'
})
export class SeriesComponent {

    private readonly _seriesDataService = inject(SeriesDataService);

    protected readonly series = toSignal(this._seriesDataService.collectionSeries$, { initialValue: [] });

    protected readonly selectedSeries = signal<ISeriesRecord | null>(null);
    protected readonly seriesIsSelected = (series: ISeriesRecord) => {
        const selectedId = this.selectedSeries()?.series_id ?? this.selectedSeries()?.url;
        const seriesId = this.selectedSeries()?.series_id ? series.series_id : series.url; // fix url to series_id
        return selectedId === seriesId && selectedId !== undefined;
    };

    protected getVolumeStatusColor(volume: IVolume) {
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

    protected navTo(url: string) {
        window.open(url, '_blank');
    }

    protected showVolumeDetails(series: ISeriesRecord) {
        if (this.seriesIsSelected(series)) {
            this.selectedSeries.set(null);
        }
        else {
            this.selectedSeries.set(series);
        }
    }

}
