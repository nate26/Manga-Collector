import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, EMPTY, map, Observable, tap, of, throwError, share } from 'rxjs';
// import { CollectionData } from '../../../archive/app.models';
import { AuthorizerService } from './authorizer.service';
import { ISeriesEditionParsed } from '../interfaces/iSeries.interface';
import { IManga } from '../interfaces/iManga.interface';
import { ICollectionResponse } from '../interfaces/iCollection.interface';

@Injectable({
    providedIn: 'root'
})
export class CollectionService {

    private serviceURL = 'http://localhost:8050'; //'https://syrrzyi0qf.execute-api.us-east-2.amazonaws.com/v1';
    private defaultCoverURL = 'https://drupal.nypl.org/sites-drupal/default/files/styles/medium/public/blogs/sJ3CT4V.gif';

    defaultSeries = { title: 'Unknown', series_id: 'unknown', editions: {} };
    defaultEdition = { edition: 'Unknown', edition_id: 'unknown', format: 'Unknown', volumes: [] };

    constructor(private http: HttpClient, private authorizer: AuthorizerService) { }

    addItems(items: any[], newItems: boolean): Observable<any[]> {
        if (this.authorizer.isUserAuthorized() && items && items.length > 0) {
            // return this.http.post<CollectionData[]>(this.serviceURL + '/add-collection', items.map(item => {
            //     const record =  {
            //         user_id: 'f69c759a-00dd-4dbe-8e58-96cd7a05969e',
            //         isbn: item.isbn,
            //         state: item.state,
            //         purchaseDate: item.purchaseDate,
            //         cost: item.cost,
            //         merchant: item.merchant,
            //         giftToMe: item.giftToMe,
            //         read: item.read,
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
        console.log('deleting...',keys, keys.length)
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

    getCollectionAsSeries(userId: string): Observable<ISeriesEditionParsed[]> {
        return this.getCollection(userId).pipe(
            map((data: ICollectionResponse) => {
                const editions: ISeriesEditionParsed[] = []
                data.lists.series.map(seriesId => data.ref.series_data[seriesId]).forEach(series => {
                    editions.push(...Object.values(series.editions).map(edition => {
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
                })
                return editions.sort((a, b) => (a.title + a.edition) < (b.title + b.edition) ? -1 : 1);
            })
        )
    }

    getCollectionAsVolume(userId: string): Observable<IManga[]> {
        return this.getCollection(userId).pipe(
            map((data: ICollectionResponse) => {
                return this.sortVolumes(
                    data.lists.volumes.slice(0, 200).map(isbn => data.ref.volume_data[isbn]).map(vol => {
                        vol.primary_cover = this.getPrimaryCoverImage(vol);
                        return vol;
                    }),
                    data
                );
            })
        );
    }

    private getCollection(userId: string): Observable<ICollectionResponse> {
        return this.http.get<ICollectionResponse>(this.serviceURL + '/user-collection?user_id=' + userId).pipe(
            share(),
            tap(console.log),
            catchError((err: any, caught: Observable<ICollectionResponse>) => {
                alert('Could not get Library... ' + err)
                return throwError(() => new Error(err));
            })
        );
    }

    private getPrimaryCoverImage(vol: IManga): string {
        if (!vol) return this.defaultCoverURL;
        // move to service
        const covers = vol.cover_images ? vol.cover_images : [];
        const primary = covers.find(cover => cover.name == 'primary');
        return primary ? primary.url : (covers.length > 0 ? covers[0].url : this.defaultCoverURL);
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
