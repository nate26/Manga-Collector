import { Component, computed, inject, model, signal } from '@angular/core';
import {
    SaleDataService,
    ShopQuery,
} from '../../services/data/sale-data.service';
import { MatDialog } from '@angular/material/dialog';
import { VolumeCoverTextComponent } from '../../common/volume-cover-text/volume-cover-text.component';
import { VolumeDetailsComponent } from '../../common/components/volume-details/volume-details.component';
import { FormsModule } from '@angular/forms';
import { AsyncPipe } from '@angular/common';
import { switchMap } from 'rxjs';
import { toObservable } from '@angular/core/rxjs-interop';

@Component({
    selector: 'app-browse-sales',
    standalone: true,
    imports: [AsyncPipe, FormsModule, VolumeCoverTextComponent],
    templateUrl: './browse-sales.component.html',
    styleUrl: './browse-sales.component.css',
})
export class BrowseSalesComponent {
    private readonly _dialog = inject(MatDialog);
    private readonly _saleDataService = inject(SaleDataService);

    // SELECT distinct(unnest(themes)) from series
    promoOptions = [
        '',
        'Black Friday',
        'Holiday Sale Week 3',
        "Crunchyroll's Price",
        'Solo Leveling Sale',
        'Free Crunchyroll Pin with $150+ Purchase!',
        'Bundle Price',
        'Clearance - Final Sale',
    ];

    orderBy = model('name');
    offset = signal(0);
    disablePrevious = computed(() => this.offset() === 0);

    filterStore = model('Crunchyroll');
    filterCondition = model('New');
    filterInStock = model('In Stock');
    filterPromo = model<string>('Black Friday');
    filterOnSale = model(true);
    filterExclusive = model(false);
    filterBundle = model<boolean>();

    filter = computed(
        () =>
        ({
            order_by: this.orderBy(),
            limit: 100,
            offset: this.offset(),
            store: this.filterStore(),
            condition: this.filterCondition(),
            stock: this.filterInStock(),
            promo: this.filterPromo(),
            on_sale: this.filterOnSale(),
            exclusive: this.filterExclusive(),
            bundle: this.filterBundle(),
        } as ShopQuery)
    );

    items$ = toObservable(this.filter).pipe(
        switchMap(query => this._saleDataService.getSaleVolumes$(query))
    );

    submitFilter() {
        this.offset.set(0);
    }

    next() {
        // TODO check if over max
        this.offset.update((offset) => offset + 100);
    }

    previous() {
        this.offset.update((offset) => Math.max(0, offset - 100));
    }

    openVolumeDetails(isbn: string) {
        this._dialog.open(VolumeDetailsComponent, { data: isbn });
    }
}
