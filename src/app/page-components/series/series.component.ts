import {
    Component,
    computed,
    ElementRef,
    inject,
    model,
    signal,
    ViewChild
} from '@angular/core';
import {
    SeriesDataService,
    SeriesQuery,
    SeriesVolume
} from '../../services/data/series-data.service';
import { AsyncPipe, NgStyle } from '@angular/common';
import { LazyImageDirective } from '../../common/directives/lazy-image/lazy-image.directive';
import { VolumeDetailsComponent } from '../../common/components/volume-details/volume-details.component';
import { MatDialog } from '@angular/material/dialog';
import { tap } from 'rxjs';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { APIQueryService } from '../../services/data/api-query.service';

@Component({
    selector: 'app-series',
    standalone: true,
    imports: [NgStyle, FormsModule, AsyncPipe, LazyImageDirective],
    templateUrl: './series.component.html',
    styleUrl: './series.component.css'
})
export class SeriesComponent {
    private readonly _router = inject(Router);
    private readonly _activatedRoute = inject(ActivatedRoute);
    private readonly _dialog = inject(MatDialog);
    private readonly _seriesDataService = inject(SeriesDataService);
    private readonly _apiQueryService = inject(APIQueryService);

    @ViewChild('display_items') displayItems!: ElementRef;

    options = this._apiQueryService.options$;

    orderBy = model('title');
    offset = signal(0);
    disablePrevious = computed(() => this.offset() === 0);

    filterTitle = model<string>();
    filterCategory = model<string>();
    filterStatus = model<string>();
    filterGenre = model<string>();
    filterTheme = model<string>();
    filterAuthor = model<string>();
    filterPublisher = model<string>();

    filter = computed(
        () =>
            ({
                order_by: this.orderBy(),
                limit: 100,
                offset: this.offset(),
                title: this.filterTitle(),
                category: this.filterCategory(),
                status: this.filterStatus(),
                genre: this.filterGenre(),
                theme: this.filterTheme(),
                author: this.filterAuthor(),
                publisher: this.filterPublisher()
            }) as SeriesQuery
    );

    series$ = this._activatedRoute.queryParams.pipe(
        tap(query => {
            this.orderBy.set(query['order_by'] || 'title');
            this.offset.set(+(query['offset'] || 0));
            this.filterTitle.set(query['title'] || '');
            this.filterCategory.set(query['category'] || '');
            this.filterStatus.set(query['status'] || '');
            this.filterGenre.set(query['genre'] || '');
            this.filterTheme.set(query['theme'] || '');
            this.filterAuthor.set(query['author'] || '');
            this.filterPublisher.set(query['publisher'] || '');
        }),
        this._seriesDataService.seriesSearch,
        tap(() =>
            this.displayItems.nativeElement.scroll({
                top: 0,
                left: 0,
                behavior: 'instant'
            } as ScrollToOptions)
        )
    );

    routeByQuery() {
        this._router.navigate([], {
            queryParams: {
                ...Object.fromEntries(
                    Object.entries(this.filter()).filter(([, v]) => Boolean(v))
                )
            }
        });
    }

    submitFilter() {
        this.offset.set(0);
        this.routeByQuery();
    }

    next() {
        // TODO check if over max
        this.offset.update(offset => offset + 100);
        this.routeByQuery();
    }

    previous() {
        this.offset.update(offset => Math.max(0, offset - 100));
        this.routeByQuery();
    }

    openSeriesDetails(series_id: string) {
        this._router.navigate(['series', series_id]);
    }

    openVolumeDetails(isbn: string) {
        this._dialog.open(VolumeDetailsComponent, { data: isbn });
    }

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
}
