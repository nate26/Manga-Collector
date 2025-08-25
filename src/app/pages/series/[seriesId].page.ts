import { Dialog } from '@angular/cdk/dialog';
import { AsyncPipe, DatePipe, NgStyle, TitleCasePipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { from, map, mergeMap, scan, shareReplay, switchMap } from 'rxjs';
import { CoverImageComponent } from '../../common/components/cover-image/cover-image.component';
import { VolumeDetailsComponent } from '../../common/components/volume-details/volume-details.component';
import { VolumeCoverTextComponent } from '../../common/volume-cover-text/volume-cover-text.component';
import {
  SeriesDataService,
  SeriesDetails,
  SeriesOutput
} from '../../services/data/series-data.service';

@Component({
  selector: 'app-series-details',
  imports: [
    NgStyle,
    AsyncPipe,
    TitleCasePipe,
    DatePipe,
    VolumeCoverTextComponent,
    CoverImageComponent
  ],
  templateUrl: './series-details.component.html',
  styleUrl: './series-details.component.css'
})
export class SeriesDetailsComponent {
  private readonly _route = inject(Router);
  private readonly _activatedRoute = inject(ActivatedRoute);
  private readonly _dialog = inject(Dialog);
  private readonly _seriesDataService = inject(SeriesDataService);

  headerLabels: { header: string; field: keyof SeriesOutput }[] = [
    { header: 'Category', field: 'category' },
    { header: 'Release Status', field: 'status' }
  ];

  statLabels: { header: string; field: keyof SeriesOutput }[] = [
    { header: 'Rating', field: 'bayesian_rating' },
    { header: 'Rank', field: 'rank' },
    { header: 'Latest Chapter', field: 'latest_chapter' }
  ];

  series$ = this._activatedRoute.params.pipe(
    map(params => params['series_id']),
    switchMap(series_id => this._seriesDataService.getSeries(series_id)),
    map(series => ({
      ...series,
      authors: this.combineSeriesDetails(series.authors),
      publishers: this.combineSeriesDetails(series.publishers),
      release_status: series.release_status
        ?.replaceAll('\\~', '~')
        ?.split('**S')
        ?.flatMap(
          (status, i) => (i ? 'S' : '') + status.replaceAll(' +', ',').replaceAll('**', '').trim()
        )
    })),
    shareReplay(1)
  );

  recommendations$ = this.series$.pipe(
    switchMap(series =>
      from(series.recommendations).pipe(
        mergeMap(recommendation => this._seriesDataService.getSeries(recommendation)),
        scan((acc, series) => [...acc, series], [] as SeriesOutput[])
      )
    )
  );

  combineSeriesDetails = (details: SeriesDetails[]) =>
    Object.entries(
      details.reduce(
        (acc, x) => ({
          ...acc,
          [x.type]: [...(acc[x.type] ?? []), x.name]
        }),
        {} as Record<string, string[]>
      )
    ).map(([type, names]) => ({ type, names }));

  openSeriesDetails(series_id: string) {
    this._route.navigate(['series', series_id]);
  }

  openSeriesSearch(column: string, keyword: string) {
    this._route.navigate(['series'], {
      queryParams: { [column]: keyword, order_by: 'title', limit: 100 }
    });
  }

  openVolumeDetails(isbn: string) {
    this._dialog.open(VolumeDetailsComponent, { data: isbn });
  }
}
