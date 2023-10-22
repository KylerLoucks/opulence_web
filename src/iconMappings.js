import { reactive, readonly} from "vue"


const colors = {
    "legendary": "#ff0000",
    "epic": "#ffb600",
    "very_rare": "#ad00fd",
    "rare": "#2799ff",
    "uncommon": "#3aad3d",
    "common": "#ffffff"
}


const iconMappings = reactive({
  arcane_arrow: colors.very_rare,
  arcane_elixir: colors.common,
  arcane_key: colors.common,
  arcane_rune: colors.uncommon,
  arcane_sphere: colors.rare,
  crystal_amulet: colors.very_rare,
  default: colors.common,
  elemental_scroll: colors.uncommon,
  nature_elixir: colors.uncommon,
  fire_ember: colors.uncommon,
  magic_coal: colors.rare,
  pixel_elixir: colors.legendary,
  solor_glyph: colors.uncommon,
  solar_sphere: colors.common,
  spellbook: colors.common,
  light_sphere: colors.epic,
  dust_sphere: colors.rare,
  starfall_cascade: colors.epic,
  starfire: colors.rare,
  wind_elixir: colors.common,
  wind_hand: colors.rare,
  wizard: colors.uncommon,
  dark_staff: colors.very_rare,
  dark_cloak: colors.very_rare,
  solar_water_sphere: colors.legendary,
  aether_sword: colors.legendary

})

export default {
  state: readonly(iconMappings)
}