defmodule MangaService.CollectionDB do
  @moduledoc """
  The CollectionDB context.
  """

  import Ecto.Query, warn: false
  alias MangaService.Repo

  alias MangaService.CollectionDB.Collection

  @doc """
  Returns the list of collection.

  ## Examples

      iex> list_collection()
      [%Collection{}, ...]

  """
  def list_collection(params) do
    Collection
    |> join(:inner, [c], v in assoc(c, :volume))
    |> order_by(^filter_order_by(params["order_by"]))
    |> where(^filter_where(params))
    |> limit(^(params["limit"] || 100))
    |> offset(^(params["offset"] || 0))
    |> Repo.all()
    |> Repo.preload(:volume)
  end

  defp filter_order_by("name_desc"),
    do: [desc: dynamic([_, v], v.display_name)]

  defp filter_order_by("name"),
    do: [asc: dynamic([_, v], v.display_name)]

  defp filter_order_by(_),
    do: []

  defp filter_where(params) do
    Enum.reduce(params, dynamic(true), fn
      {"name", value}, dynamic ->
        dynamic(
          [_, v],
          ^dynamic and fragment("lower(?) like '%' || lower(?) || '%'", v.display_name, ^value)
        )

      {"user_id", value}, dynamic ->
        dynamic([c], ^dynamic and c.user_id == ^value)

      {"collection", value}, dynamic ->
        dynamic([c], ^dynamic and c.collection == ^value)

      {"category", value}, dynamic ->
        dynamic([_, v], ^dynamic and v.category == ^value)

      {"volume", value}, dynamic ->
        dynamic([_, v], ^dynamic and v.volume == ^value)

      {"cost_le", value}, dynamic ->
        dynamic([c], ^dynamic and c.cost <= ^value)

      {"cost_ge", value}, dynamic ->
        dynamic([c], ^dynamic and c.cost >= ^value)

      {"store", value}, dynamic ->
        dynamic([c], ^dynamic and c.store == ^value)

      {"purchase_date_le", value}, dynamic ->
        dynamic([c], ^dynamic and c.purchase_date <= ^value)

      {"purchase_date_ge", value}, dynamic ->
        dynamic([c], ^dynamic and c.purchase_date >= ^value)

      {"read", value}, dynamic ->
        dynamic([c], ^dynamic and c.read == ^value)

      {"tags", value}, dynamic ->
        dynamic([c], ^dynamic and (fragment("? = ANY(?)", ^value, c.tags) or ^value == ""))

      {_, _}, dynamic ->
        dynamic
    end)
  end

  def sublist?([], _), do: false

  def sublist?(l1 = [_ | t], l2) do
    List.starts_with?(l1, l2) or sublist?(t, l2)
  end

  @doc """
  Gets a single collection.

  Raises `Ecto.NoResultsError` if the Collection does not exist.

  ## Examples

      iex> get_collection!(123)
      %Collection{}

      iex> get_collection!(456)
      ** (Ecto.NoResultsError)

  """
  def get_collection_by_id(id) do
    Repo.get_by(Collection, %{collection_id: id})
    |> Repo.preload(:volume)
  end

  @doc """
  Gets collection data for a volume by isbn.

  Raises `Ecto.NoResultsError` if the Collection does not exist.

  ## Examples

      iex> get_collection_by_user_id!("9781427816702", "user_id")
      %Collection{}

      iex> get_collection_by_user_id!("", "user_id")
      ** (Ecto.NoResultsError)

  """
  def get_collections_by_user_id(params) do
    # TODO offset and limit and filters
    Collection
    |> where([c], c.isbn == ^params["isbn"] and c.user_id == ^params["user_id"])
    |> Repo.all()
    |> Repo.preload(:volume)
  end

  @doc """
  Creates a collection.

  ## Examples

      iex> create_collection(%{field: value})
      {:ok, %Collection{}}

      iex> create_collection(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_collection(attrs \\ %{}) do
    %Collection{}
    |> Collection.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a collection.

  ## Examples

      iex> update_collection(collection, %{field: new_value})
      {:ok, %Collection{}}

      iex> update_collection(collection, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_collection(%Collection{} = collection, attrs) do
    collection
    |> Collection.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a collection.

  ## Examples

      iex> delete_collection(collection)
      {:ok, %Collection{}}

      iex> delete_collection(collection)
      {:error, %Ecto.Changeset{}}

  """
  def delete_collection(%Collection{} = collection) do
    Repo.delete(collection)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking collection changes.

  ## Examples

      iex> change_collection(collection)
      %Ecto.Changeset{data: %Collection{}}

  """
  def change_collection(%Collection{} = collection, attrs \\ %{}) do
    Collection.changeset(collection, attrs)
  end
end
