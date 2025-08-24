import { Dialog } from '@angular/cdk/dialog';
import { AsyncPipe } from '@angular/common';
import { Component, computed, ElementRef, inject, model, signal, viewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { ToggleSwitchModule } from 'primeng/toggleswitch';
import { switchMap, tap } from 'rxjs';
import { VolumeDetailsComponent } from '../../common/components/volume-details/volume-details.component';
import { VolumeCoverTextComponent } from '../../common/volume-cover-text/volume-cover-text.component';
import { SaleDataService, ShopQuery } from '../../services/data/sale-data.service';

@Component({
  selector: 'app-browse-sales',
  imports: [AsyncPipe, FormsModule, InputTextModule, ToggleSwitchModule, VolumeCoverTextComponent],
  templateUrl: './browse-sales.component.html',
  styleUrl: './browse-sales.component.css'
})
export class BrowseSalesComponent {
  private readonly _router = inject(Router);
  private readonly _activatedRoute = inject(ActivatedRoute);
  private readonly _dialog = inject(Dialog);
  private readonly _saleDataService = inject(SaleDataService);

  readonly displayItems = viewChild.required<ElementRef>('display_items');

  // SELECT distinct(unnest(themes)) from series
  promoOptions = [
    '',
    'Black Friday',
    'Holiday Sale Week 3',
    "Crunchyroll's Price",
    'Solo Leveling Sale',
    'Free Crunchyroll Pin with $150+ Purchase!',
    'Bundle Price',
    'Clearance - Final Sale'
  ];

  orderBy = model('name');
  offset = signal(0);
  disablePrevious = computed(() => this.offset() === 0);

  filterName = model<string>();
  filterStore = model('Crunchyroll');
  filterCondition = model('New');
  filterInStock = model('In Stock');
  filterPromo = model<string>('Black Friday');
  filterOnSale = model(true);
  filterExclusive = model(false);
  filterBundle = model<boolean | string>();

  filter = computed(
    () =>
      ({
        order_by: this.orderBy(),
        limit: 100,
        offset: this.offset(),
        name: this.filterName(),
        store: this.filterStore(),
        condition: this.filterCondition(),
        stock: this.filterInStock(),
        promo: this.filterPromo(),
        on_sale: this.filterOnSale(),
        exclusive: this.filterExclusive(),
        bundle: this.filterBundle()
      }) as ShopQuery
  );

  items$ = this._activatedRoute.queryParams.pipe(
    tap(query => {
      this.orderBy.set(query['order_by'] || 'name');
      this.offset.set(+query['offset'] || 0);
      this.filterName.set(query['name'] || '');
      this.filterStore.set(query['store'] || '');
      this.filterCondition.set(query['condition'] || '');
      this.filterInStock.set(query['stock'] || '');
      this.filterPromo.set(query['promo'] || '');
      this.filterOnSale.set(query['on_sale'] === 'true');
      this.filterExclusive.set(query['exclusive'] === 'true');
      this.filterBundle.set(
        query['bundle'] === 'true' ? true : query['bundle'] === 'false' ? false : ''
      );
    }),
    switchMap(query => this._saleDataService.getSaleVolumes$(query)),
    tap(() =>
      this.displayItems().nativeElement.scroll({
        top: 0,
        left: 0,
        behavior: 'instant'
      } as ScrollToOptions)
    )
  );

  routeByQuery() {
    this._router.navigate([], {
      queryParams: {
        ...Object.fromEntries(Object.entries(this.filter()).filter(([, v]) => Boolean(v)))
      }
    });
  }

  submitFilter() {
    this.offset.set(0);
    this.routeByQuery();
  }

  next() {
    // TODO check if over max
    this.offset.update(offset => offset + 100);
    this.routeByQuery();
  }

  previous() {
    this.offset.update(offset => Math.max(0, offset - 100));
    this.routeByQuery();
  }

  openVolumeDetails(isbn: string) {
    this._dialog.open(VolumeDetailsComponent, { data: isbn });
  }
}
