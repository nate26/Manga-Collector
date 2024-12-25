import { Component, inject } from '@angular/core';
import { SeriesDataService, SeriesOutput } from '../../services/data/series-data.service';
import { VolumeDetailsComponent } from '../../common/components/volume-details/volume-details.component';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { map } from 'rxjs';
import { AsyncPipe, DatePipe, TitleCasePipe } from '@angular/common';

@Component({
    selector: 'app-series-details',
    standalone: true,
    imports: [AsyncPipe, TitleCasePipe, DatePipe],
    templateUrl: './series-details.component.html',
    styleUrl: './series-details.component.css'
})
export class SeriesDetailsComponent {

    private readonly _activatedRoute = inject(ActivatedRoute);
    private readonly _dialog = inject(MatDialog);
    private readonly _seriesDataService = inject(SeriesDataService);

    headerLabels: { header: string; field: keyof SeriesOutput }[] = [{ header: "Category", field: "category" }, { header: "Release Status", field: "status" }];

    series$ = this._activatedRoute.params.pipe(
        map(params => params['series_id']),
        this._seriesDataService.series
    );

    openVolumeDetails(isbn: string) {
        this._dialog.open(VolumeDetailsComponent, { data: isbn });
    }

}
