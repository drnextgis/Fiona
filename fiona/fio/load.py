"""$ fio load"""


from functools import partial
import itertools
import json
import logging

import click
import cligj

import fiona
from fiona.fio import options
from fiona.transform import transform_geom


FIELD_TYPES_MAP_REV = dict([(v, k) for k, v in fiona.FIELD_TYPES_MAP.items()])


@click.command(short_help="Load GeoJSON to a dataset in another format.")
@click.argument('output', required=True)
@click.option('-f', '--format', '--driver', required=True,
              help="Output format driver name.")
@options.src_crs_opt
@click.option('--dst-crs', '--dst_crs',
              help="Destination CRS.  Defaults to --src-crs when not given.")
@cligj.features_in_arg
@click.option('--layer', metavar="INDEX|NAME", callback=options.cb_layer,
              help="Load features into specified layer.  Layers use "
                   "zero-based numbering when accessed by index.")
@click.pass_context
def load(ctx, output, driver, src_crs, dst_crs, features, layer):
    """Load features from JSON to a file in another format.

    The input is a GeoJSON feature collection or optionally a sequence of
    GeoJSON feature objects."""
    verbosity = (ctx.obj and ctx.obj['verbosity']) or 2
    logger = logging.getLogger('fio')

    dst_crs = dst_crs or src_crs

    if src_crs and dst_crs and src_crs != dst_crs:
        transformer = partial(transform_geom, src_crs, dst_crs,
                              antimeridian_cutting=True, precision=-1)
    else:
        transformer = lambda x: x

    def feature_gen():
        for feat in features:
            feat['geometry'] = transformer(feat['geometry'])
            yield feat

    try:
        source = feature_gen()

        # Use schema of first feature as a template.
        # TODO: schema specified on command line?
        first = next(source)
        schema = {'geometry': first['geometry']['type']}
        schema['properties'] = dict([
            (k, FIELD_TYPES_MAP_REV.get(type(v)) or 'str')
            for k, v in first['properties'].items()])

        with fiona.drivers(CPL_DEBUG=verbosity > 2):
            with fiona.open(
                    output, 'w',
                    driver=driver,
                    crs=dst_crs,
                    schema=schema,
                    layer=layer) as dst:
                dst.write(first)
                dst.writerecords(source)

    except Exception:
        logger.exception("Exception caught during processing")
        raise click.Abort()
