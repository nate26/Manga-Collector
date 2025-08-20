import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, catchError, map, of, shareReplay, switchMap, tap, throwError } from 'rxjs';
import { IVolume, Volume } from '../../interfaces/iVolume.interface';
import { UserService } from './user.service';

@Injectable({
  providedIn: 'root'
})
export class VolumeService {
  readonly #http = inject(HttpClient);
  readonly #userService = inject(UserService);

  getVolume(isbn: string) {
    return this.#http.get<Volume>('http://localhost:4000/api/volume/' + isbn);
  }

  readonly volumesBasic$: Observable<IVolume[]> = of({ error: Error('no gql'), data: null } as any)
    // this.apollo
    //   .watchQuery<IGQLAllRecord>({
    //     query: this.VOLUMES_BASIC_QUERY,
    //     variables: { user_id: null }
    //   })
    //   .valueChanges
    .pipe(
      tap(({ error }) => {
        if (error) throw error;
      }),
      map(response => response.data.all_records.records),
      shareReplay(),
      catchError(err =>
        throwError(() => Error('Could not get all volumes because ' + err.message, err))
      )
    );

  queryVolume(isbn: string): Observable<IVolume> {
    return of(this.#userService.userData()).pipe(
      switchMap(
        ({ user_id }) => of({ error: Error('no gql'), data: null } as any)
        // this.apollo.watchQuery<IGQLGetRecord>({
        //   query: this.SINGLE_VOLUME_QUERY,
        //   variables: { isbn, user_id }
        // }).valueChanges
      ),
      tap(({ error }) => {
        if (error) throw error;
      }),
      map(response => response.data.get_record.record!),
      catchError(err =>
        throwError(() => new Error('Could not get all volumes because ' + err.message, err))
      )
    );
  }
}
