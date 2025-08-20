defmodule MangaService.ShopsDB do
  @moduledoc """
  The ShopsDB context.
  """

  import Ecto.Query, warn: false
  alias MangaService.Repo

  alias MangaService.ShopsDB.Shop

  @doc """
  Returns the list of shops.

  ## Examples

      iex> list_shops()
      [%Shop{}, ...]

  """
  def list_shops(params) do
    Shop
    |> join(:inner, [p], v in assoc(p, :volume))
    |> order_by(^filter_order_by(params["order_by"]))
    |> where(^filter_where(params))
    |> limit(^(params["limit"] || 100))
    |> offset(^(params["offset"] || 0))
    |> Repo.all()
    |> Repo.preload([:volume, :market])
  end

  defp filter_order_by("name_desc"),
    do: [desc: dynamic([_, v], v.display_name)]

  defp filter_order_by("name"),
    do: [asc: dynamic([_, v], v.display_name)]

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
      {"name", value}, dynamic ->
        dynamic(
          [_, v],
          ^dynamic and fragment("lower(?) like '%' || lower(?) || '%'", v.display_name, ^value)
        )

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
  def get_shop(id), do: Repo.get(Shop, id)

  @doc """
  Gets a single volume shop data by id.

  Raises `Ecto.NoResultsError` if the Shop does not exist.

  ## Examples

      iex> get_shop_by_id!("123412341234112341234")
      %Shop{}

      iex> get_shop_by_id!("123412341234112341234")
      ** (Ecto.NoResultsError)

  """
  def get_shop_by_id(item_id), do: Repo.get_by(Shop, %{item_id: item_id})

  @doc """
  Gets a single volume shop data by isbn.

  Raises `Ecto.NoResultsError` if the Shop does not exist.

  ## Examples

      iex> get_shop_by_isbn!("9781427816702")
      %Shop{}

      iex> get_shop_by_isbn!("9781427816702")
      ** (Ecto.NoResultsError)

  """
  def get_shops_by_isbn(isbn) do
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

  def distinct(key) do
    query =
      from(v in Shop,
        select: v.promotion,
        distinct: true
      )

    Repo.all(query)
  end
end
