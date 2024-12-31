import { AsyncPipe, CurrencyPipe, DatePipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { LazyImageDirective } from '../../directives/lazy-image/lazy-image.directive';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { VolumeService } from '../../../services/data/volume.service';

@Component({
    selector: 'app-volume-details',
    standalone: true,
    imports: [AsyncPipe, DatePipe, CurrencyPipe, LazyImageDirective],
    templateUrl: './volume-details.component.html',
    styleUrl: './volume-details.component.css'
})
export class VolumeDetailsComponent {
    private readonly _volumeService = inject(VolumeService);

    volume$ = this._volumeService.getVolume(inject<string>(MAT_DIALOG_DATA));
}
