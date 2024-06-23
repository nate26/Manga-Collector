import { Component, computed, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { SeriesDataService } from '../../services/data/series-data.service';
import { IVolume } from '../../interfaces/iVolume.interface';
import { NgClass, NgStyle } from '@angular/common';
import { ISeriesRecord } from '../../interfaces/iSeries.interface';

@Component({
    selector: 'app-series',
    standalone: true,
    imports: [NgStyle, NgClass],
    templateUrl: './series.component.html',
    styleUrl: './series.component.css'
})
export class SeriesComponent {

    seriesDataService = inject(SeriesDataService);

    series = toSignal(this.seriesDataService.collectionSeries$, { initialValue: [] });
    url = computed(() => this.series()[0]?.cover_image);

    selectedSeries = signal<ISeriesRecord | null>(null);

    seriesIsSelected = (series: ISeriesRecord) => {
        const selectedId = this.selectedSeries()?.series_id ?? this.selectedSeries()?.url;
        const seriesId = this.selectedSeries()?.series_id ? series.series_id : series.url; // fix url to series_id
        return selectedId === seriesId && selectedId !== undefined;
    }

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

    showVolumeDetails(series: ISeriesRecord) {
        if (this.seriesIsSelected(series)) {
            this.selectedSeries.set(null);
        }
        else {
            this.selectedSeries.set(series);
        }
    }

}
