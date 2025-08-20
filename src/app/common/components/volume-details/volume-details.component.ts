import { DIALOG_DATA } from '@angular/cdk/dialog';
import { AsyncPipe, DatePipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { VolumeService } from '../../../services/data/volume.service';
import { LazyImageDirective } from '../../directives/lazy-image/lazy-image.directive';

@Component({
  selector: 'app-volume-details',
  imports: [AsyncPipe, DatePipe, LazyImageDirective],
  templateUrl: './volume-details.component.html',
  styleUrl: './volume-details.component.css'
})
export class VolumeDetailsComponent {
  private readonly _volumeService = inject(VolumeService);

  volume$ = this._volumeService.getVolume(inject<string>(DIALOG_DATA));
}
