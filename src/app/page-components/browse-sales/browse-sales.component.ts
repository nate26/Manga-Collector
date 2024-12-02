import { Component, computed, inject, model, signal } from '@angular/core';
import { SaleDataService, ShopQuery } from '../../services/data/sale-data.service';
import { MatDialog } from '@angular/material/dialog';
import { VolumeCoverTextComponent } from '../../common/volume-cover-text/volume-cover-text.component';
import { VolumeDetailsComponent } from '../../common/components/volume-details/volume-details.component';
import { FormsModule } from '@angular/forms';
import { AsyncPipe } from '@angular/common';

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

    promoOptions = ['', 'Black Friday', 'Clearance - Final Sale', 'Crunchyroll\'s Price'];

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

    filter = computed(() => ({
        order_by: this.orderBy(),
        limit: 100,
        offset: this.offset(),
        store: this.filterStore(),
        condition: this.filterCondition(),
        stock: this.filterInStock(),
        promo: this.filterPromo(),
        on_sale: this.filterOnSale(),
        exclusive: this.filterExclusive(),
        bundle: this.filterBundle()
    } as ShopQuery));

    items$ = this._saleDataService.getSaleVolumes$(this.filter());

    updateData() {
        this.items$ = this._saleDataService.getSaleVolumes$(this.filter());
    }

    submitFilter() {
        this.offset.set(0);
        this.updateData();
    }

    next() {
        // TODO check if over max
        this.offset.update((offset) => offset + 100);
        this.updateData();
    }

    previous() {
        this.offset.update((offset) => Math.max(0, offset - 100));
        this.updateData();
    }

    openVolumeDetails(isbn: string) {
        this._dialog.open(VolumeDetailsComponent, { data: isbn });
    }
}
