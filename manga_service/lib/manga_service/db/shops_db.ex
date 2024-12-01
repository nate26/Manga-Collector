defmodule MangaService.ShopsDB do
  @moduledoc """
  The ShopsDB context.
  """

  import Ecto.Query, warn: false
  alias MangaService.Repo

  alias MangaService.ShopsDB.Shop
  alias MangaService.VolumesDB.Volume

  @doc """
  Returns the list of shops.

  ## Examples

      iex> list_shops()
      [%Shop{}, ...]

  """
  def list_shops(params) do
    Shop
    |> order_by(^filter_order_by(params["order_by"]))
    |> where(^filter_where(params))
    |> limit(^(params["limit"] || 100))
    |> offset(^(params["offset"] || 0))
    # |> join(:full, [s], v in Volume, on: s.isbn == v.isbn)
    # |> join(:full, [s], assoc(s, :volume), as: :volume)
    |> Repo.all()
  end

  defp filter_order_by("price_desc"),
    do: [desc: dynamic([p], p.price)]

  defp filter_order_by("price"),
    do: [asc: dynamic([p], p.price)]

  defp filter_order_by("promotion_percentage_desc"),
    do: [desc: dynamic([p], p.promotion_percentage)]

  defp filter_order_by("promotion_percentage"),
    do: [asc: dynamic([p], p.promotion_percentage)]

  defp filter_order_by(_),
    do: []

  defp filter_where(params) do
    Enum.reduce(params, dynamic(true), fn
      {"store", value}, dynamic ->
        dynamic([p], ^dynamic and p.store == ^value)

      {"condition", value}, dynamic ->
        dynamic([p], ^dynamic and p.condition == ^value)

      {"stock", value}, dynamic ->
        dynamic([p], ^dynamic and p.stock_status == ^value)

      {"promo", value}, dynamic ->
        dynamic([p], ^dynamic and p.promotion == ^value)

      {"on_sale", value}, dynamic ->
        dynamic([p], ^dynamic and p.is_on_sale == ^value)

      {"exclusive", value}, dynamic ->
        dynamic([p], ^dynamic and p.exclusive == ^value)

      {"bundle", value}, dynamic ->
        dynamic([p], ^dynamic and p.is_bundle == ^value)

      {"price", value}, dynamic ->
        dynamic([p], ^dynamic and p.price == ^value)

      {"price_le", value}, dynamic ->
        dynamic([p], ^dynamic and p.price <= ^value)

      {"price_lt", value}, dynamic ->
        dynamic([p], ^dynamic and p.price < ^value)

      {"price_ge", value}, dynamic ->
        dynamic([p], ^dynamic and p.price >= ^value)

      {"price_gt", value}, dynamic ->
        dynamic([p], ^dynamic and p.price > ^value)

      {"promo_perc", value}, dynamic ->
        dynamic([p], ^dynamic and p.promotion_percentage == ^value)

      {"promo_perc_le", value}, dynamic ->
        dynamic([p], ^dynamic and p.promotion_percentage <= ^value)

      {"promo_perc_lt", value}, dynamic ->
        dynamic([p], ^dynamic and p.promotion_percentage < ^value)

      {"promo_perc_ge", value}, dynamic ->
        dynamic([p], ^dynamic and p.promotion_percentage >= ^value)

      {"promo_perc_gt", value}, dynamic ->
        dynamic([p], ^dynamic and p.promotion_percentage > ^value)

      {_, _}, dynamic ->
        dynamic
    end)
  end

  @doc """
  Gets a single shop.

  Raises `Ecto.NoResultsError` if the Shop does not exist.

  ## Examples

      iex> get_shop!(123)
      %Shop{}

      iex> get_shop!(456)
      ** (Ecto.NoResultsError)

  """
  def get_shop!(id), do: Repo.get!(Shop, id)

  @doc """
  Gets a single volume shop data by isbn.

  Raises `Ecto.NoResultsError` if the Shop does not exist.

  ## Examples

      iex> get_shop_by_isbn!("9781427816702")
      %Shop{}

      iex> get_shop_by_isbn!("9781427816702")
      ** (Ecto.NoResultsError)

  """
  def get_shop_by_id!(item_id) do
    query =
      from(v in Shop,
        where: v.item_id == ^item_id,
        select: v
      )

    Repo.one(query)
  end

  @doc """
  Gets a single volume shop data by isbn.

  Raises `Ecto.NoResultsError` if the Shop does not exist.

  ## Examples

      iex> get_shop_by_isbn!("9781427816702")
      %Shop{}

      iex> get_shop_by_isbn!("9781427816702")
      ** (Ecto.NoResultsError)

  """
  def get_shops_by_isbn!(isbn) do
    query =
      from(v in Shop,
        where: v.isbn == ^isbn,
        select: v
      )

    Repo.all(query)
  end

  @doc """
  Creates a shop.

  ## Examples

      iex> create_shop(%{field: value})
      {:ok, %Shop{}}

      iex> create_shop(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_shop(attrs \\ %{}) do
    %Shop{}
    |> Shop.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a shop.

  ## Examples

      iex> update_shop(shop, %{field: new_value})
      {:ok, %Shop{}}

      iex> update_shop(shop, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_shop(%Shop{} = shop, attrs) do
    shop
    |> Shop.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a shop.

  ## Examples

      iex> delete_shop(shop)
      {:ok, %Shop{}}

      iex> delete_shop(shop)
      {:error, %Ecto.Changeset{}}

  """
  def delete_shop(%Shop{} = shop) do
    Repo.delete(shop)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking shop changes.

  ## Examples

      iex> change_shop(shop)
      %Ecto.Changeset{data: %Shop{}}

  """
  def change_shop(%Shop{} = shop, attrs \\ %{}) do
    Shop.changeset(shop, attrs)
  end
end
