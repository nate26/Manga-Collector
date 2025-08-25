import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, catchError, of, shareReplay, throwError } from 'rxjs';
import { Volume } from './volume.type';

@Injectable({
  providedIn: 'root'
})
export class VolumeService {
  readonly #http = inject(HttpClient);

  getVolume(isbn: string) {
    return this.#http.get<Volume>('http://localhost:4000/api/volume/' + isbn);
  }

  readonly volumesBasic$: Observable<Volume[]> = of([]).pipe(
    shareReplay(),
    catchError(err =>
      throwError(() => Error('Could not get all volumes because ' + err.message, err))
    )
  );
}
