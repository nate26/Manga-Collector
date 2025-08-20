import { AsyncPipe, CurrencyPipe, DatePipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { Volume } from '../../../interfaces/iVolume.interface';
import { LazyImageDirective } from '../../directives/lazy-image/lazy-image.directive';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';

@Component({
    selector: 'app-volume-details',
    standalone: true,
    imports: [AsyncPipe, DatePipe, CurrencyPipe, LazyImageDirective],
    templateUrl: './volume-details.component.html',
    styleUrl: './volume-details.component.css',
})
export class VolumeDetailsComponent {
    private readonly _http = inject(HttpClient);

    volume$ = this._http
        .get<Volume>(
            'http://localhost:4000/api/volume/' +
            inject<string>(MAT_DIALOG_DATA)
        );
}
