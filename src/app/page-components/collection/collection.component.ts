import { Dialog } from '@angular/cdk/dialog';
import { AsyncPipe, CurrencyPipe, TitleCasePipe } from '@angular/common';
import {
  Component,
  DestroyRef,
  ElementRef,
  computed,
  inject,
  model,
  signal,
  viewChild
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { BehaviorSubject, combineLatest, map, switchMap, tap } from 'rxjs';
import { VolumeDetailsComponent } from '../../common/components/volume-details/volume-details.component';
import { LazyImageDirective } from '../../common/directives/lazy-image/lazy-image.directive';
import { SearchVolumesComponent } from '../../common/search-volumes/search-volumes.component';
import { TagListComponent } from '../../common/tag-list/tag-list.component';
import {
  CollectionDataService,
  CollectionInput,
  CollectionOutput,
  CollectionQuery,
  Volume
} from '../../services/data/collection-data.service';
import { UserService } from '../../services/data/user.service';

@Component({
  selector: 'app-collection',
  imports: [
    AsyncPipe,
    TitleCasePipe,
    CurrencyPipe,
    FormsModule,
    InputTextModule,
    SearchVolumesComponent,
    TagListComponent,
    LazyImageDirective
  ],
  templateUrl: './collection.component.html',
  styleUrl: './collection.component.css'
})
export class CollectionComponent {
  private readonly _router = inject(Router);
  private readonly _activatedRoute = inject(ActivatedRoute);
  private readonly _dialog = inject(Dialog);
  private readonly _collectionDataService = inject(CollectionDataService);
  private readonly _destroy = inject(DestroyRef);
  private readonly userService = inject(UserService);

  readonly displayItems = viewChild.required<ElementRef>('display_items');

  availableCategories = ['light-novels', 'novels', 'manga', 'manga-bundles', 'manhwa', 'manhua'];
  availableStores = [
    'Amazon',
    'Barnes And Noble',
    'Crunchyroll',
    'RightStuf',
    'Kinokuniya',
    'In Stock Trades',
    'Other'
  ];

  orderBy = model('name');
  offset = signal(0);
  disablePrevious = computed(() => this.offset() === 0);

  filterCollection = model<string>('Collection');
  filterName = model<string>();
  filterCategory = model<string>(); // ? options
  filterVolume = model<string>();
  filterCost = model<number>(); // ? slider
  filterStore = model<string>(); // ? options
  filterPurchaseDate = model<string>(); // ? slider
  filterRead = model<boolean>(false);
  filterTags = model<string[]>([]); // ? autocomplete?

  filter = computed(
    () =>
      ({
        order_by: this.orderBy(),
        limit: 100,
        offset: this.offset(),
        collection: this.filterCollection(),
        name: this.filterName(),
        category: this.filterCategory(),
        volume: this.filterVolume(),
        cost_ge: this.filterCost(),
        store: this.filterStore(),
        purchase_date_le: this.filterPurchaseDate(),
        read: this.filterRead(),
        tags: this.filterTags()
      }) as CollectionQuery
  );

  canUserEdit = computed(() => this.userService.canUserEdit());

  reQuery$ = new BehaviorSubject<void>(undefined);
  collections$ = combineLatest({
    query: this._activatedRoute.queryParams,
    trigger: this.reQuery$
  }).pipe(
    map(({ query }) => query),
    tap(query => {
      this.orderBy.set(query['order_by'] || 'name');
      this.offset.set(+(query['offset'] || 0));
      this.filterCollection.set(query['collection'] || '');
      this.filterName.set(query['name'] || '');
      this.filterCategory.set(query['category'] || '');
      this.filterVolume.set(query['volume'] || '');
      this.filterCost.set(+(query['cost_ge'] || 0));
      this.filterStore.set(query['store'] || '');
      this.filterPurchaseDate.set(query['purchase_date_le'] || '');
      this.filterRead.set(query['read'] === 'true');
      this.filterTags.set(query['tags'] ? query['tags'].split(',') : []);
    }),
    switchMap(query => this._collectionDataService.getCollectionVolumes(query)),
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

  createCollection(vol: Volume) {
    this._collectionDataService
      .createCollection(vol.isbn)
      .pipe(takeUntilDestroyed(this._destroy))
      .subscribe({
        next: () => this.reQuery$.next(),
        error: err => {
          console.error(err);
          alert(
            'could not add volume ' + vol.display_name + ' to collection. Please try again later.'
          );
        }
      });
  }

  updateValue(item: CollectionOutput, key: keyof CollectionOutput, event: Event) {
    this.updateCollection(
      item.collection_id,
      { [key]: this.getEventVal(event) },
      item.volume.display_name
    );
  }

  updateTags(item: CollectionOutput, tags: string[]) {
    this.updateCollection(item.collection_id, { tags }, item.volume.display_name);
  }

  updateCollection(
    collection_id: string,
    collection: Partial<CollectionInput>,
    display_name: string
  ) {
    this._collectionDataService
      .updateCollection(collection_id, collection)
      .pipe(takeUntilDestroyed(this._destroy))
      .subscribe({
        error: err => {
          console.error(err);
          alert(
            'could not update volume ' + display_name + ' in collection. Please try again later.'
          );
        }
      });
  }

  deleteCollection(collection: CollectionOutput) {
    this._collectionDataService
      .deleteCollection(collection.collection_id)
      .pipe(takeUntilDestroyed(this._destroy))
      .subscribe({
        next: () => this.reQuery$.next(),
        error: err => {
          console.error(err);
          alert(
            'could not delete volume ' +
              collection.volume.display_name +
              ' from collection. Please try again later.'
          );
        }
      });
  }

  getEventVal(value: Event) {
    const target = (
      value as InputEvent & {
        target: {
          type: string;
          checked: boolean;
          value: string;
        };
      }
    ).target;
    return target.type === 'checkbox' ? (target.checked ? 'YES' : 'NO') : target.value;
  }

  openVolumeDetails(isbn: string) {
    this._dialog.open(VolumeDetailsComponent, { data: isbn });
  }
}
