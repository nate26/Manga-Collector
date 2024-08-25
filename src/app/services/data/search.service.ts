import { inject, Injectable } from '@angular/core';
import { gql, Apollo } from 'apollo-angular';
import { Observable, catchError, filter, map, switchMap, tap, throwError } from 'rxjs';
import { IGQLSearchVolumes } from '../../interfaces/iGQLRequests.interface';

@Injectable({
    providedIn: 'root'
})
export class SearchService {

    private readonly _apollo = inject(Apollo);

    private readonly SEARCH_VOLUMES_QUERY = gql`
        query volume_search($search: String!) {
            volume_search(search: $search) {
                records {
                    isbn
                    series
                    display_name
                    primary_cover_image_url
                }
                success
                errors
            }
        }
    `;

    readonly searchVolumes$ = (search$: Observable<string | null>) => search$.pipe(
        filter(search => Boolean(search)),
        switchMap(search => this._apollo.watchQuery<IGQLSearchVolumes>({
            query: this.SEARCH_VOLUMES_QUERY,
            variables: { search }
        }).valueChanges),
        tap(({ error }) => {
            if (error) throw error;
        }),
        map(response => response.data.volume_search.records),
        catchError((err) => throwError(() => new Error('Could not get search data because ', err)))
    );
}
