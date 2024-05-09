import { HttpClient } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { toObservable } from '@angular/core/rxjs-interop';
import { catchError, EMPTY, map, Observable, tap, of, throwError, switchMap, shareReplay, filter } from 'rxjs';
import { AuthorizerService } from './authorizer.service';
import { ISeriesEditionParsed } from '../interfaces/iSeries.interface';
import { IManga } from '../interfaces/iManga.interface';
import { ICollection, ICollectionResponse } from '../interfaces/iCollection.interface';

@Injectable({
    providedIn: 'root'
})
export class CollectionService {

    private serviceURL = 'http://localhost:8050';
    private defaultCoverURL = 'https://drupal.nypl.org/sites-drupal/default/files/styles/medium/public/blogs/sJ3CT4V.gif';

    // get user ID
    readonly userId = signal('');

    // get user collection by ID / share result
    private readonly _collection$ = toObservable(this.userId).pipe(
        filter(id => Boolean(id)),
        switchMap(userId => this.http.get<ICollectionResponse>(this.serviceURL + '/user-collection?user_id=' + userId)),
        shareReplay(),
        catchError((err: Error) => {
            alert('Could not get Library... ' + err.message);
            return throwError(() => new Error(err.message)); // validate
        })
    );

    // get sorted user collection
    readonly collectionAsVolume$ = this._collection$.pipe(
        map((data: ICollectionResponse) => {
            return this.sortVolumes(
                // maps volume isbn to full data object
                // get primary cover
                data.lists.volumes.map(isbn => data.ref.volume_data[isbn]).map(vol => {
                    vol.primary_cover = this.getPrimaryCoverImage(vol);
                    return vol;
                }),
                data
            ).slice(0, 50);
        })
    );

    // Gets all user collection editions with enriched volume data
    readonly collectionAsSeries$ = this._collection$.pipe(
        map((data: ICollectionResponse) => {
            const editions: ISeriesEditionParsed[] = [];
            // maps series IDs to ISeries
            data.lists.series.map(seriesId => data.ref.series_data[seriesId]).forEach(series => {
                // gets all editions from series / update cover to primary or a default
                editions.push(...Object.values(series.editions).map(edition => {
                    // enrich volume data from edition volumes
                    const volumes = edition.volumes.map(vol => data.ref.volume_data[vol.isbn] || vol);
                    return {
                        edition: edition.edition,
                        edition_id: edition.edition_id,
                        format: edition.format,
                        title: series.title,
                        cover: volumes.length > 0 ? this.getPrimaryCoverImage(volumes[0]) : this.defaultCoverURL,
                        volumes: volumes
                    }
                }));
            });
            // sort editions
            return editions.sort((a, b) => (a.title + a.edition) < (b.title + b.edition) ? -1 : 1);
        })
    );


    constructor(private http: HttpClient, private authorizer: AuthorizerService) { }

    addItems(items: ICollection[]): Observable<ICollection[]> {
        if (this.authorizer.isUserAuthorized() && items && items.length > 0) {
            // return this.http.post<CollectionData[]>(this.serviceURL + '/add-collection', items.map(item => {
            //     const record =  {
            //         ...item,
            //         user_id: this.userId(),
            //         tags: item.tags ? item.tags : [],
            //     } as CollectionData;
            //     if (!newItems) {
            //         record.id = item.id;
            //         record.inserted = item.inserted;
            //         record.updated = item.updated;
            //     }
            //     return record;
            // })).pipe(
            return of('adding...').pipe(
                tap({
                    next: data => console.log(data),
                    error: err => alert(JSON.stringify(err))
                }),
                map(() => items)
            );
        } else {
            return EMPTY;
        }
    }

    removeItems(keys: { id: string, user_id: string }[]): Observable<string> {
        console.log('deleting...', keys, keys.length)
        if (this.authorizer.isUserAuthorized() && keys && keys.length > 0) {
            // return this.http.post<string>(this.serviceURL + '/delete-collection', keys).pipe(
            return of('deleting...').pipe(
                tap({
                    next: data => console.log(data),
                    error: err => alert(JSON.stringify(err))
                })
            );
        } else {
            return EMPTY;
        }
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    private getPrimaryCoverImage(vol: IManga): string {
        if (!vol) return this.defaultCoverURL;
        // // move to service
        const covers = vol.cover_images ? vol.cover_images : [];
        const primary = covers.find(cover => cover.name == 'primary');
        return primary ? primary.url.replace('www', 'legacy') : (covers.length > 0 ? covers[0].url.replace('www', 'legacy') : this.defaultCoverURL);
        // const img = 'https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/nx99022-Hh2WdyNgR8HM.jpg';
        // return primary ? img : this.defaultCoverURL;
    }

    private sortVolumes(manga: IManga[], data: ICollectionResponse): IManga[] {
        const getSortString = (item: IManga) => {
            try {
                const series = data.ref.series_data[item.series_id];
                return series.title + series.editions[item.edition_id].edition + item.format + item.volume;
            }
            catch {
                return '';
            }
        }
        return manga.sort((a, b) => getSortString(a) < getSortString(b) ? -1 : 1)
    }
}
