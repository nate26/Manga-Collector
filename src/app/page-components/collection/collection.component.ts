import { Component, DestroyRef, computed, inject, model, signal } from '@angular/core';
import { AsyncPipe, CurrencyPipe, NgClass, TitleCasePipe } from '@angular/common';
import { Collection, CollectionDataService, CollectionQuery } from '../../services/data/collection-data.service';
import { takeUntilDestroyed, toObservable } from '@angular/core/rxjs-interop';
import { ICollection } from '../../interfaces/iCollection.interface';
import { SearchVolumesComponent } from '../../common/search-volumes/search-volumes.component';
import { IVolume } from '../../interfaces/iVolume.interface';
import { VolumeService } from '../../services/data/volume.service';
import { forkJoin, switchMap, tap } from 'rxjs';
import { ITheme } from '../../interfaces/iSeries.interface';
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
        NgClass,
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
    private readonly _volumeService = inject(VolumeService);
    private readonly _destroy = inject(DestroyRef);
    protected readonly userService = inject(UserService);

    availableCategories = ['light-novels', 'novels', 'manga', 'manga-bundles', 'manhwa', 'manhua'];
    // TODO change B&N to BarnesAndNoble
    availableStores = ['Amazon', 'Barnes And Noble', 'Crunchyroll', 'RightStuf', 'Kinokuniya', 'In Stock Trades', 'Other'];

    protected editSwitch = signal(false);
    protected isEditing = computed(
        () => this.editSwitch() && this.userService.userDataIsValid()
    );

    // TODO change this to immediate saves? and add batch save later
    newVolumes = signal<IVolume[]>([]);
    saveBatch = signal<ICollection[]>([]); // temp cache of save changes
    saved = signal<ICollection[]>([]); // cache of all prior saved records
    deleteBatch = signal<string[]>([]); // temp cache of delete changes
    deleted = signal<string[]>([]); // cache of all prior deleted records


    orderBy = model('name');
    offset = signal(0);

    // consider reactive forms instead of template forms
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
            // TODO tags: this.filterTags()
        } as CollectionQuery)
    );

    /*
    // separate filter and saved states for performance
    editedVolumes = computed(() => {
        const vols = this.volumes();
        if (!vols) return [];
        return [
            // add in all new volumes in current batch
            ...this.saveBatch()
                .filter((record) => !record.id)
                .map((volume) => {
                    return {
                        ...this.newVolumes().find(
                            (vol) => vol.isbn === volume.isbn
                        )!,
                        user_collection_data: [volume],
                        edited: true,
                    };
                }),
            // add in all new volumes that were previously saved
            ...this.saved()
                .filter((record) => this.volumeIDs().indexOf(record.id) === -1)
                .map((volume) => {
                    return {
                        ...this.newVolumes().find(
                            (vol) => vol.isbn === volume.isbn
                        )!,
                        user_collection_data: [volume],
                        edited: Boolean(
                            this.saveBatch().find(
                                (record) => record.id === volume.id
                            )
                        ),
                    };
                }),
            // modify all existing volumes that were edited
            ...vols.map((volume) => {
                const editedState = this.saveBatch().find(
                    (record) => record.id === volume.user_collection_data[0].id
                );
                const savedState = this.saved().find(
                    (record) => record.id === volume.user_collection_data[0].id
                );
                const changed = editedState || savedState;
                if (changed) {
                    return {
                        ...volume,
                        user_collection_data: [changed],
                        edited: Boolean(editedState),
                    };
                }
                return { ...volume, edited: false };
            }),
        ].filter(
            (vol) =>
                [...this.deleteBatch(), ...this.deleted()].indexOf(
                    vol.user_collection_data[0].id ?? ''
                ) === -1
        ); // remove deleted records
    });

    filteredVolumes = computed(() => {
        return this.editedVolumes().filter((volume) => {
            const record = volume.user_collection_data[0];
            // check name
            return (
                (!this.filterName() ||
                    (volume.name ?? '')
                        .toLowerCase()
                        .includes(this.filterName().toLowerCase())) &&
                // check category
                (this.filterCategory() === '' ||
                    volume.category + '' === this.filterCategory() + '') &&
                // check volume
                (!this.filterVolume() ||
                    volume.volume === this.filterVolume()) &&
                // check cost
                (!this.filterCost() ||
                    record.cost.toString() === this.filterCost()) &&
                // check merchant
                (this.filterMerchant() === '' ||
                    record.merchant + '' === this.filterMerchant()) &&
                // check purchaseDate
                (!this.filterPurchaseDate() ||
                    (record.purchaseDate ?? '')
                        .toLowerCase()
                        .includes(this.filterPurchaseDate().toLowerCase())) &&
                // check read
                (this.filterRead() === '' ||
                    record.read === (this.filterRead() === 'YES')) &&
                // check giftToMe
                (this.filterGiftToMe() === '' ||
                    record.giftToMe === (this.filterGiftToMe() === 'YES')) &&
                // check tags
                (this.filterTags().length === 0 ||
                    this.filterTags().some((fTag) =>
                        record.tags.some(
                            (tag) => fTag.toLowerCase() === tag.toLowerCase()
                        )
                    ))
            );
        });
    });
    */

    collections$ = toObservable(this.filter).pipe(
        switchMap(query => this._collectionDataService.getCollectionVolumes$(query))
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

    // TODO check below for what can be removed

    parseThemes = (themes: ITheme[]) => themes.map((t) => t.theme).join(', ');

    private _batchEdit(batch: ICollection[], record: ICollection) {
        // update batch if record is already in batch
        if (
            batch.some(
                (b) => (b.id ?? b.temp_id) === (record.id ?? record.temp_id)
            )
        ) {
            // update existing if was previously saved
            return batch.map((existingRecord) =>
                (existingRecord.id ?? existingRecord.temp_id) ===
                    (record.id ?? record.temp_id)
                    ? record
                    : existingRecord
            );
        }

        if (
            !record.id &&
            this.saved().some(
                (savedRecord) => savedRecord.temp_id === record.temp_id
            )
        ) {
            // remove from saved if we are re-editing it
            this.saved.update((saved) =>
                saved.filter(
                    (savedRecord) => savedRecord.temp_id !== record.temp_id
                )
            );
        }

        // add to batch if not already there
        return [...batch, record];
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    doEdit(index: number, field: string, value: Event) {
        // this.saveBatch.update((batch) => {
        //     const existingRecord =
        //         this.filteredVolumes()[index].user_collection_data[0];
        //     const newValue = this.getEventVal(value);
        //     let parsedValue;
        //     if (field === 'cost') parsedValue = parseFloat(newValue);
        //     else if (field === 'read' || field === 'giftToMe')
        //         parsedValue = (<HTMLInputElement>value.target).checked;
        //     else parsedValue = newValue;
        //     return this._batchEdit(batch, {
        //         ...existingRecord,
        //         [field]: parsedValue,
        //     });
        // });
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    editTags(index: number, value: string[]): void {
        // this.saveBatch.update((batch) => {
        //     return this._batchEdit(batch, {
        //         ...this.filteredVolumes()[index].user_collection_data[0],
        //         tags: value,
        //     });
        // });
    }

    markForDelete(record: Collection) {
        if (record.collection_id) {
            this.deleteBatch.update((batch) => [...batch, record.collection_id!]);
        } else {
            // TODO
            // this.saveBatch.update((batch) =>
            //     batch.filter((r) => r.temp_id !== record.temp_id)
            // );
        }
    }

    save() {
        forkJoin({
            saveResult: this._collectionDataService
                .saveToCollection(this.saveBatch())
                .pipe(
                    tap({
                        next: (saveResult) => {
                            console.log(
                                'The following records were saved: ',
                                this.saveBatch()
                            );
                            // merge with existing cache
                            this.saved.update((currSaved) =>
                                saveResult.reduce(
                                    (acc, record) =>
                                        this._batchEdit(acc, record),
                                    currSaved
                                )
                            );
                            this.saveBatch.set([]);
                        },
                    })
                ),
            deleteResult: this._collectionDataService
                .deleteFromCollection(this.deleteBatch())
                .pipe(
                    tap({
                        next: (deleteResult) => {
                            console.log(
                                'The following records were deleted: ',
                                this.deleteBatch()
                            );
                            // merge with existing cache
                            this.deleted.update((currDeleted) => [
                                ...new Set([...currDeleted, ...deleteResult]),
                            ]);
                            this.deleteBatch.set([]);
                        },
                    })
                ),
        })
            .pipe(takeUntilDestroyed(this._destroy))
            .subscribe({
                next: () => {
                    this.stopEditing();
                    this.editSwitch.set(false);
                },
            });
    }

    stopEditing() {
        this.saveBatch.set([]);
        this.editSwitch.set(false);
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

    addVolume(vol: IVolume) {
        const addToBatch = () =>
            this.saveBatch.update((batch) => [
                ...batch,
                this._collectionDataService.buildNewRecord(vol),
            ]);
        if (this.newVolumes().find((v) => v.isbn === vol.isbn)) {
            addToBatch();
        } else {
            // fetch if not in existing cache
            this._volumeService
                .queryVolume(vol.isbn)
                .pipe(takeUntilDestroyed(this._destroy))
                .subscribe({
                    next: (volume) => {
                        this.newVolumes.update((volumes) => [
                            ...volumes,
                            volume,
                        ]);
                        addToBatch();
                    },
                    error: (err) => {
                        console.error(err);
                        alert(
                            'could not get volume data for ' +
                            vol.display_name +
                            'to add to collection'
                        );
                    },
                });
        }
    }

    openVolumeDetails(isbn: string) {
        this._dialog.open(VolumeDetailsComponent, { data: isbn });
    }
}
