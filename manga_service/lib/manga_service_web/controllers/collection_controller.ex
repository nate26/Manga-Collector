defmodule MangaServiceWeb.CollectionController do
  use Phoenix.Controller, formats: [:json]
  alias MangaService.CollectionDB

  def index(conn, params) do
    collections = CollectionDB.list_collection(params)

    json(
      conn,
      collections
      |> Enum.map(fn collection ->
        %{
          collection_id: collection.collection_id,
          collection: collection.collection,
          cost: collection.cost,
          store: collection.store,
          purchase_date: collection.purchase_date,
          read: collection.read,
          tags: collection.tags,
          volume: %{
            isbn: collection.volume.isbn,
            name: collection.volume.name,
            display_name: collection.volume.display_name,
            category: collection.volume.category,
            volume: collection.volume.volume,
            brand: collection.volume.brand,
            series: %{
              title: collection.volume.series,
              # TODO
              url: ""
            },
            series_id: collection.volume.series_id,
            edition: collection.volume.edition,
            edition_id: collection.volume.edition_id,
            release_date: collection.volume.release_date,
            primary_cover_image: collection.volume.primary_cover_image
          }
        }
      end)
    )
  end

  def show(conn, %{"id" => collection_id}) do
    collection = CollectionDB.get_collection_by_id(collection_id)

    case collection do
      nil ->
        raise "No record found for ID"

      _ ->
        json(
          conn,
          %{
            collection_id: collection.collection_id,
            collection: collection.collection,
            cost: collection.cost,
            store: collection.store,
            purchase_date: collection.purchase_date,
            read: collection.read,
            tags: collection.tags,
            volume: %{
              isbn: collection.volume.isbn,
              name: collection.volume.name,
              display_name: collection.volume.display_name,
              category: collection.volume.category,
              volume: collection.volume.volume,
              brand: collection.volume.brand,
              series: %{
                title: collection.volume.series,
                # TODO
                url: ""
              },
              series_id: collection.volume.series_id,
              edition: collection.volume.edition,
              edition_id: collection.volume.edition_id,
              release_date: collection.volume.release_date,
              primary_cover_image: collection.volume.primary_cover_image
            }
          }
        )
    end
  end

  def create(conn, %{"collection" => collection_params}) do
    case CollectionDB.create_collection(collection_params) do
      {:ok, collection} ->
        conn
        |> put_status(:created)
        |> json(%{
          id: collection.id,
          collection_id: collection.collection_id,
          user_id: collection.user_id,
          isbn: collection.isbn,
          read: collection.read,
          store: collection.store,
          collection: collection.collection,
          cost: collection.cost,
          purchase_date: collection.purchase_date,
          tags: collection.tags,
          rating: collection.rating,
          inserted_at: collection.inserted_at,
          updated_at: collection.updated_at
        })

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: changeset.errors})
    end
  end

  def update(conn, %{"id" => collection_id, "collection" => collection_params}) do
    curr_collection = CollectionDB.get_collection_by_id(collection_id)

    case CollectionDB.update_collection(curr_collection, collection_params) do
      {:ok, collection} ->
        conn
        |> put_status(:ok)
        |> json(%{
          id: collection.id,
          collection_id: collection.collection_id,
          user_id: collection.user_id,
          isbn: collection.isbn,
          read: collection.read,
          store: collection.store,
          collection: collection.collection,
          cost: collection.cost,
          purchase_date: collection.purchase_date,
          tags: collection.tags,
          rating: collection.rating,
          inserted_at: collection.inserted_at,
          updated_at: collection.updated_at
        })

      {:error, changeset} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: changeset.errors})
    end
  end

  def delete(conn, %{"id" => collection_id}) do
    collection = CollectionDB.get_collection_by_id(collection_id)

    case CollectionDB.delete_collection(collection) do
      {:ok, _} ->
        conn
        |> put_status(:ok)
        |> json(%{success: true})

      {:error, _} ->
        conn
        |> put_status(:unprocessable_entity)
        |> json(%{errors: "Unable to delete collection"})
    end
  end
end
