import { CommonModule } from '@angular/common';
import { Component, WritableSignal, signal } from '@angular/core';
import { CollectionService } from '../../services/collection.service';
import { CdkTableModule } from '@angular/cdk/table';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { CoverImageSlideshowComponent } from '../../common/cover-image-slideshow/cover-image-slideshow.component';
import { FormsModule } from '@angular/forms';
import { SeriesMap, VolumeMap, ShopMap, SeriesVolume, Series, Shop, Volume } from '../../app.component';

export interface TableColumn {
    header: string;
    key: string;
    align: string;
    width?: string;
    style?: () => { [key: string]: string };
    render?: 'text' | 'image' | 'checkbox';
}

@Component({
    selector: 'app-series-view',
    standalone: true,
    imports: [CommonModule, FormsModule, CdkTableModule, MatButtonModule, MatCheckboxModule, CoverImageSlideshowComponent],
    templateUrl: './series-view.component.html',
    styleUrl: './series-view.component.css',
    animations: [
        trigger('detailExpand', [
            state('collapsed', style({ height: '0px', minHeight: '0' })),
            state('expanded', style({ height: '*' })),
            transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
        ]),
    ]
})
export class SeriesViewComponent {

    // series$ = this.collectionService.collectionAsSeries$;



    // eslint-disable-next-line @typescript-eslint/no-var-requires
    seriesMap = {} as SeriesMap //require('../../../../bin/src/manga/series.json') as SeriesMap;
    seriesArr = Object.values(this.seriesMap);
    // series$ = this.seriesMap$.pipe(map((seriesMap) => Object.values(seriesMap)));

    // eslint-disable-next-line @typescript-eslint/no-var-requires
    volumesMap = {} as VolumeMap //require('../../../../bin/src/manga/volumes.json') as VolumeMap;
    // volumes$ = this.volumesMap$.pipe(map((volumeMap) => Object.values(volumeMap)));

    // eslint-disable-next-line @typescript-eslint/no-var-requires
    shopMap = {} as ShopMap//require('../../../../bin/src/manga/shop.json') as ShopMap;
    // shop$ = this.shopMap$.pipe(map((shopMap) => Object.values(shopMap)));



    expandedElement!: Series | null;

    seriesColumns: TableColumn[] = [
        {
            header: '',
            key: 'cover',
            align: 'center',
            width: '50px',
            render: 'image'
        },
        {
            header: 'Series',
            key: 'title',
            align: 'left'
        },
        {
            header: 'Format',
            key: 'type',
            align: 'center',
            width: '100px'
        }
    ];
    seriesColumnKeys = this.seriesColumns.map(col => col.key);

    // selectedSeries: WritableSignal<Series | undefined> = signal(undefined);
    selectedVol: WritableSignal<(Volume & Shop) | undefined> = signal(undefined);
    // updateSelectedVol = computed(() => {
    //     const row = this.selectedSeries();
    //     if (this.expandedElement === this.selectedSeries()) {
    //         // clear expansion
    //         this.expandedElement = null;
    //     }
    //     else if (row) {
    //         // set expansion data
    //         this.expandedElement = this.expandedElement === row ? null : row;
    //         this.selectVolume(row.volumes.length > 0 ? row.volumes[0] : undefined);
    //     }
    //     this.selectVolume(undefined);
    // });

    // put edit in service smh
    // editVolume = new EventEmitter<IManga>();

    constructor(private collectionService: CollectionService) { }

    getCoverImage(series: Series): string {
        return this.volumesMap[series.volumes[0].isbn].cover_images[0].url;
    }

    // getVolumeStyle(vol: IManga) {
    //     const style = {
    //         background: '',
    //         color: 'black',
    //         border: '',
    //         'text-shadow': '',
    //         'box-shadow': ''
    //     }
    //     if (vol.state == 'Pre-Order') style.background = '#f3b16b';
    //     else if (vol.state == 'Shipping') style.background = '#ff8d8d';
    //     else if (vol.state == 'OOS') style.background = '#a99eff';
    //     else if (vol.state == 'Gift') style.background = '#7dbbf3';
    //     else if (vol.read) style.background = '#2b9160';
    //     else if (vol.state == 'Owned') style.background = '#8adab4';
    //     else if (vol.stock_status == 'Out of Stock') {
    //         style.background = 'repeating-linear-gradient(135deg, #ebebeb, #ebebeb 4px, rgb(177 177 177) 5px, rgb(127 127 127) 8px)';
    //         style['text-shadow'] = '0px 0px 9px #fff, 0px 0px 9px #fff, 0px 0px 9px #fff, 0px 0px 9px #fff, 0px 0px 9px #fff, 0px 0px 9px #fff';
    //     }
    //     else if (vol.stock_status == 'Out of Print') style.background = '#a3a3a3';
    //     else style.background = '#ebebeb';

    //     if ((new Date(vol.release_date)) > (new Date())) style.color = '#e69138';

    //     if (vol.is_on_sale && !vol.purchaseDate) style.border = '3px solid rgb(219 85 85 / 60%)';

    //     if (this.selectedVol === vol) {
    //         style['box-shadow'] = '0px 0px 2px 2px #f5f5f5bf'
    //     }
    //     return style;
    // }

    getVolumeStyle(vol: SeriesVolume) {
        return {
            background: '#ebebeb',
            color: (new Date(this.volumesMap[vol.isbn].release_date)) > (new Date()) ? '#e69138' : 'black',
            border: this.shopMap[vol.isbn].shops.some(shop => shop.is_on_sale) ? '3px solid rgb(219 85 85 / 60%)' : ''
        };
    }

    getAttr(item: Series, column: TableColumn): unknown {
        return item[column.key as keyof Series]
    }

    // edit(vol: IManga) {
    //     this.editVolume.emit(vol)
    // }

    selectVolume(vol: SeriesVolume | undefined) {
        if (vol) {
            this.selectedVol.set({
                ...this.volumesMap[vol.isbn],
                ...this.shopMap[vol.isbn]
            });
        }
        else {
            this.selectedVol.set(undefined);
        }
    }

    setExpanded(row: Series): void {
        if (this.expandedElement === row) {
            // clear expansion
            this.expandedElement = null;
            this.selectVolume(undefined);
        }
        else if (row) {
            // set expansion data
            this.expandedElement = this.expandedElement === row ? null : row;
            this.selectVolume(row.volumes.length > 0 ? row.volumes[0] : undefined);
        }
    }

}
