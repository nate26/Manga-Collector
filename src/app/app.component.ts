import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { CollectionComponent } from './page-components/collection/collection.component';
import { RouterOutlet } from '@angular/router';
import { Observable, forkJoin, map, of } from 'rxjs';

export interface SeriesVolume {
    isbn: string;
    volume: string;
    category: string;
}
export interface Series {
    series_id: string;
    title: string;
    associated_titles: string[];
    url: string;
    type: string;
    series_match_confidence: number;
    volumes: SeriesVolume[];
}
export type SeriesMap = { [series_id: string]: Series };

export interface Volume {
    isbn: string;
    series: string;
    series_id: string;
    display_name: string;
    name: string;
    category: string;
    category_id: string;
    volume: string;
    url: string;
    record_added_date: Date;
    record_updated_date: Date;
    release_date: Date;
    publisher: string;
    format: string;
    pages: null;
    authors: string;
    isbn_10: string;
    cover_images: {
        name: string;
        url: string;
    }[];
    description: string;
}
export type VolumeMap = { [isbn: string]: Volume };

export interface Shop {
    isbn: string;
    retail_price: number;
    shops: {
        store: string;
        condition: string;
        url: string;
        store_price: number;
        stock_status: string;
        last_stock_update: Date;
        coupon: string;
        is_on_sale: boolean;
    }[];
}
export type ShopMap = { [isbn: string]: Shop };

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, RouterOutlet, CollectionComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})
export class AppComponent {
    title = 'Manga Tracker';

    // eslint-disable-next-line @typescript-eslint/no-var-requires
    seriesMap$ = of(require('../../bin/src/manga/series.json') as SeriesMap)
    series$ = this.seriesMap$.pipe(map((seriesMap) => Object.values(seriesMap)));

    // eslint-disable-next-line @typescript-eslint/no-var-requires
    volumesMap$ = of(require('../../bin/src/manga/volumes.json') as VolumeMap)
    volumes$ = this.volumesMap$.pipe(map((volumeMap) => Object.values(volumeMap)));

    // eslint-disable-next-line @typescript-eslint/no-var-requires
    shopMap$ = of(require('../../bin/src/manga/shop.json') as ShopMap)
    shop$ = this.shopMap$.pipe(map((shopMap) => Object.values(shopMap)));

    getCoverImage(series: Series): Observable<string> {
        return this.volumesMap$.pipe(
            map(volumeMap => volumeMap[series.volumes[0].isbn].cover_images[0].url)
        );
    }

    getVolumeStyle(vol: SeriesVolume) {
        return forkJoin({
            shopMap: this.shopMap$,
            volumeMap: this.volumesMap$
        }).pipe(
            map(({ shopMap, volumeMap }) => ({
                shopData: shopMap[vol.isbn],
                volumeData: volumeMap[vol.isbn]
            })),
            map(({ shopData, volumeData }) => ({
                background: '#ebebeb',
                color: (new Date(volumeData.release_date)) > (new Date()) ? '#e69138' : 'black',
                border: shopData.shops.some(shop => shop.is_on_sale) ? '3px solid rgb(219 85 85 / 60%)' : ''
            }))
        );
    }

}
