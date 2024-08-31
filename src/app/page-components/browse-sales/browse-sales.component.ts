import { Component, computed, effect, inject, signal } from '@angular/core';
import { SaleDataService } from '../../services/data/sale-data.service';
import { toSignal } from '@angular/core/rxjs-interop';
import { NgStyle } from '@angular/common';
import { map } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';

export type SaleVolume = {
    isbn: string;
    primary_cover_image_url: string;
    retail_price: number;
    store: string;
    store_price: number;
    is_on_sale: boolean;
    stock_status: string;
    sale_price: number;
    url: string;
};

@Component({
    selector: 'app-browse-sales',
    standalone: true,
    imports: [NgStyle],
    templateUrl: './browse-sales.component.html',
    styleUrl: './browse-sales.component.css'
})
export class BrowseSalesComponent {


    dialog = inject(MatDialog);


    e = effect(() => console.log(this.filteredVolumes()));

    private readonly _saleDataService = inject(SaleDataService);
    volumes = toSignal(this._saleDataService.saleVolumes$.pipe(
        map(volumes =>
            volumes.map(vol => {
                const bestSale = vol.purchase_options
                    .filter(shopItem => shopItem.is_on_sale)
                    .sort((a, b) => a.store_price - b.store_price)[0];
                return {
                    isbn: vol.isbn,
                    primary_cover_image_url: vol.primary_cover_image_url,
                    retail_price: vol.retail_price,
                    ...bestSale,
                    sale_price: Math.round((1 - bestSale.store_price / vol.retail_price) * 100)
                };
            })
        )
    ), { initialValue: [] });

    filteredVolumes = computed(() => this.volumes().filter(vol => {
        // const sales = vol.purchase_options.filter(shopItem => shopItem.is_on_sale);
        // return (sales.map(s => s.stock_status === 'In Stock').includes(this.filterInStock()) || !this.filterInStock())
        //     && (!this.filterNoClearance() || !this.isCrunchyrollClearance(vol))
        //     && (!this.filterClearance() || this.isCrunchyrollClearance(vol));
        return (vol.stock_status === 'In Stock' || !this.filterInStock())
            && (!this.filterNoClearance() || !this.isCrunchyrollClearance(vol))
            && (!this.filterClearance() || this.isCrunchyrollClearance(vol));
    }));
    filterInStock = signal(true);
    filterNoClearance = signal(true);
    filterClearance = signal(false);

    isCrunchyrollClearance = (vol: SaleVolume) => //volume.purchase_options.find(shopItem =>
        vol.store === 'Crunchyroll' &&
        vol.is_on_sale &&
        vol.store_price < vol.retail_price * 0.5;
    // );

    // getSalePrice = (volume: IVolume) => {
    //     const sale = volume.purchase_options
    //         .filter(shopItem => shopItem.is_on_sale)
    //         .sort((a, b) => a.store_price - b.store_price)[0];
    //     return Math.round((1 - sale.store_price / volume.retail_price) * 100);
    // };

}
