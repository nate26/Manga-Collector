import { Dialog } from '@angular/cdk/dialog';
import { AsyncPipe } from '@angular/common';
import { Component, computed, ElementRef, inject, model, signal, viewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { SkeletonModule } from 'primeng/skeleton';
import { TagModule } from 'primeng/tag';
import { switchMap, tap } from 'rxjs';
import { VolumeDetailsComponent } from '../../common/components/volume-details/volume-details.component';
import { SaleDataService, ShopQuery } from '../../services/data/sale-data.service';

@Component({
  selector: 'app-browse-sales',
  imports: [AsyncPipe, FormsModule, InputTextModule, ButtonModule, TagModule, SkeletonModule],
  templateUrl: './(browse-volumes).page.html'
})
export class BrowseVolumesPage {
  private readonly _router = inject(Router);
  private readonly _activatedRoute = inject(ActivatedRoute);
  private readonly _dialog = inject(Dialog);
  private readonly _saleDataService = inject(SaleDataService);

  readonly displayItems = viewChild.required<ElementRef>('display_items');

  orderBy = model('name');
  offset = signal(0);
  disablePrevious = computed(() => this.offset() === 0);
  filterName = model<string>();

  filter = computed<ShopQuery>(() => ({
    order_by: this.orderBy(),
    limit: 100,
    offset: this.offset(),
    name: this.filterName()
  }));

  items$ = this._activatedRoute.queryParams.pipe(
    tap(query => {
      this.orderBy.set(query['order_by'] || 'name');
      this.offset.set(+query['offset'] || 0);
      this.filterName.set(query['name'] || '');
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

  submitFilter() {
    this.offset.set(0);
    this.routeByQuery();
  }
}
