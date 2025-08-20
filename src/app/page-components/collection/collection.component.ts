import { Component, DestroyRef, computed, inject, model, signal } from '@angular/core';
import { AsyncPipe, CurrencyPipe, TitleCasePipe } from '@angular/common';
import { CollectionDataService, CollectionInput, CollectionOutput, CollectionQuery, Volume } from '../../services/data/collection-data.service';
import { takeUntilDestroyed, toObservable } from '@angular/core/rxjs-interop';
import { SearchVolumesComponent } from '../../common/search-volumes/search-volumes.component';
import { BehaviorSubject, combineLatest, map } from 'rxjs';
import { UserService } from '../../services/data/user.service';
import { TagListComponent } from '../../common/tag-list/tag-list.component';
import { LazyImageDirective } from '../../common/directives/lazy-image/lazy-image.directive';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { VolumeDetailsComponent } from '../../common/components/volume-details/volume-details.component';
import { FormsModule } from '@angular/forms';

@Component({
    selector: 'app-collection',
    standalone: true,
    imports: [
        AsyncPipe,
        TitleCasePipe,
        CurrencyPipe,
        FormsModule,
        MatDialogModule,
        SearchVolumesComponent,
        TagListComponent,
        LazyImageDirective,
    ],
    templateUrl: './collection.component.html',
    styleUrl: './collection.component.css',
})
export class CollectionComponent {
    private readonly _dialog = inject(MatDialog);
    private readonly _collectionDataService = inject(CollectionDataService);
    private readonly _destroy = inject(DestroyRef);
    private readonly userService = inject(UserService);

    availableCategories = ['light-novels', 'novels', 'manga', 'manga-bundles', 'manhwa', 'manhua'];
    availableStores = ['Amazon', 'Barnes And Noble', 'Crunchyroll', 'RightStuf', 'Kinokuniya', 'In Stock Trades', 'Other'];

    orderBy = model('name');
    offset = signal(0);

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
        } as CollectionQuery)
    );

    canUserEdit = computed(() => this.userService.canUserEdit());

    reQuery$ = new BehaviorSubject<void>(undefined);
    collections$ = combineLatest({
        query: toObservable(this.filter),
        trigger: this.reQuery$
    }).pipe(
        map(({ query }) => query),
        this._collectionDataService.collectionSearch
    );

    next() {
        // TODO check if over max
        this.offset.update((offset) => offset + 100);
    }

    previous() {
        this.offset.update((offset) => Math.max(0, offset - 100));
    }

    createCollection(vol: Volume) {
        this._collectionDataService
            .createCollection(vol.isbn)
            .pipe(takeUntilDestroyed(this._destroy))
            .subscribe({
                next: () => this.reQuery$.next(),
                error: (err) => {
                    console.error(err);
                    alert(
                        'could not add volume ' +
                        vol.display_name +
                        ' to collection. Please try again later.'
                    );
                },
            });
    }

    updateValue(item: CollectionOutput, key: keyof CollectionOutput, event: Event) {
        this.updateCollection(item.collection_id, { [key]: this.getEventVal(event) }, item.volume.display_name);
    }

    updateTags(item: CollectionOutput, tags: string[]) {
        this.updateCollection(item.collection_id, { tags }, item.volume.display_name);
    }

    updateCollection(collection_id: string, collection: Partial<CollectionInput>, display_name: string) {
        this._collectionDataService
            .updateCollection(collection_id, collection)
            .pipe(takeUntilDestroyed(this._destroy))
            .subscribe({
                error: (err) => {
                    console.error(err);
                    alert(
                        'could not update volume ' +
                        display_name +
                        ' in collection. Please try again later.'
                    );
                },
            });
    }

    deleteCollection(collection: CollectionOutput) {
        this._collectionDataService
            .deleteCollection(collection.collection_id)
            .pipe(takeUntilDestroyed(this._destroy))
            .subscribe({
                next: () => this.reQuery$.next(),
                error: (err) => {
                    console.error(err);
                    alert(
                        'could not delete volume ' +
                        collection.volume.display_name +
                        ' from collection. Please try again later.'
                    );
                },
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
        return target.type === 'checkbox'
            ? target.checked
                ? 'YES'
                : 'NO'
            : target.value;
    }

    openVolumeDetails(isbn: string) {
        this._dialog.open(VolumeDetailsComponent, { data: isbn });
    }
}
