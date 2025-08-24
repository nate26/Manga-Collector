import { Component, computed, inject, model, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { ToggleSwitchModule } from 'primeng/toggleswitch';
import { switchMap, tap } from 'rxjs';
import { SaleDataService, ShopQuery } from '../../../services/data/sale-data.service';

@Component({
  selector: 'app-filter-popover',
  imports: [FormsModule, InputTextModule, ToggleSwitchModule],
  templateUrl: './filter-popover.component.html',
  styleUrl: './filter-popover.component.css'
})
export class FilterPopoverComponent {
  private readonly _router = inject(Router);
  private readonly _activatedRoute = inject(ActivatedRoute);
  private readonly _saleDataService = inject(SaleDataService);

  // TODO NGRX
  offset = signal(0);
  orderBy = model('name');

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
    switchMap(query => this._saleDataService.getSaleVolumes$(query))
    // tap(() =>
    //   this.displayItems().nativeElement.scroll({
    //     top: 0,
    //     left: 0,
    //     behavior: 'instant'
    //   } as ScrollToOptions)
    // )
  );

  submitFilter() {
    this.offset.set(0);
    this.routeByQuery();
  }

  routeByQuery() {
    this._router.navigate([], {
      queryParams: {
        ...Object.fromEntries(Object.entries(this.filter()).filter(([, v]) => Boolean(v)))
      }
    });
  }
}
