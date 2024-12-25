import { Component, computed, ElementRef, inject, model, signal, ViewChild } from '@angular/core';
import { SeriesDataService, SeriesVolume } from '../../services/data/series-data.service';
import { AsyncPipe, NgStyle } from '@angular/common';
import { LazyImageDirective } from '../../common/directives/lazy-image/lazy-image.directive';
import { VolumeDetailsComponent } from '../../common/components/volume-details/volume-details.component';
import { MatDialog } from '@angular/material/dialog';
import { tap } from 'rxjs';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
    selector: 'app-series',
    standalone: true,
    imports: [NgStyle, AsyncPipe, LazyImageDirective],
    templateUrl: './series.component.html',
    styleUrl: './series.component.css'
})
export class SeriesComponent {

    private readonly _route = inject(Router);
    private readonly _activatedRoute = inject(ActivatedRoute);
    private readonly _dialog = inject(MatDialog);
    private readonly _seriesDataService = inject(SeriesDataService);

    @ViewChild('display_items') displayItems!: ElementRef;

    orderBy = model('name');
    offset = signal(0);
    disablePrevious = computed(() => this.offset() === 0);

    filterTitle = model<string>();

    series$ = this._activatedRoute.queryParams.pipe(
        tap(query => {
            this.orderBy.set(query['order_by'] || 'name');
            this.offset.set(+(query['offset'] || 0));
            this.filterTitle.set(query['title'] || '');
        }),
        this._seriesDataService.seriesSearch,
        tap(() => this.displayItems.nativeElement.scroll({
            top: 0,
            left: 0,
            behavior: 'instant'
        } as ScrollToOptions))
    );

    protected getVolumeStatusColor(volume: SeriesVolume) {
        // if (volume.user_collection_data.length > 0) {
        //     return { 'background-color': '#A6F7CD' }; //CDA6F7
        // }
        if (volume.stock_status === 'In Stock') {
            return { 'background-color': '#EBEBEB' };
        }
        if (volume.stock_status === 'Pre-Order') {
            return { 'background-color': '#F7CDA6' };
        }
        if (volume.stock_status === 'Backorder') {
            return { 'background-color': '#8b5cf6' };
        }
        if (volume.stock_status === 'Out of Print') {
            return { 'background-color': '#929292' };
        }
        return { 'background-color': '#C4C4C4' };

    }

    openSeriesDetails(series_id: string) {
        this._route.navigate(['series', series_id]);
    }

    openVolumeDetails(isbn: string) {
        this._dialog.open(VolumeDetailsComponent, { data: isbn });
    }

}
