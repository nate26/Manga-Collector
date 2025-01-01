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
    SeriesQuery
} from '../../services/data/series-data.service';
import { AsyncPipe } from '@angular/common';
import { VolumeDetailsComponent } from '../../common/components/volume-details/volume-details.component';
import { MatDialog } from '@angular/material/dialog';
import { map, tap } from 'rxjs';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import {
    APIQueryService,
    BrowseOptions
} from '../../services/data/api-query.service';
import { AutofillSelectFilterComponent } from '../../common/components/filters/autofill-select-filter/autofill-select-filter.component';
import {
    NumberRange,
    NumberRangeFilterComponent
} from '../../common/components/filters/number-range-filter/number-range-filter.component';
import { CoverImageComponent } from '../../common/components/cover-image/cover-image.component';

@Component({
    selector: 'app-series',
    standalone: true,
    imports: [
        FormsModule,
        AsyncPipe,
        CoverImageComponent,
        AutofillSelectFilterComponent,
        NumberRangeFilterComponent
    ],
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
    filterRating = model<NumberRange>();
    filterRank = model<NumberRange>();

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
                publisher: this.filterPublisher(),
                rating_ge: this.filterRating()?.min,
                rating_le: this.filterRating()?.max,
                rank_ge: this.filterRank()?.min,
                rank_le: this.filterRank()?.max
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
            this.filterRating.set({
                min: query['rating_ge'] ? +query['rating_ge'] : undefined,
                max: query['rating_le'] ? +query['rating_le'] : undefined
            });
            this.filterRank.set({
                min: query['rank_ge'] ? +query['rank_ge'] : undefined,
                max: query['rank_le'] ? +query['rank_le'] : undefined
            });
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

    options$(key: keyof BrowseOptions) {
        return this._apiQueryService.options$.pipe(map(o => o[key]));
    }

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
}
