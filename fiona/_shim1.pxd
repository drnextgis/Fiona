include "ogrext1.pxd"

ctypedef enum OGRFieldSubType:
    OFSTNone = 0
    OFSTBoolean = 1
    OFSTInt16 = 2
    OFSTFloat32 = 3
    OFSTMaxSubType = 3

cdef bint is_field_null(void *feature, int n)
cdef void set_field_null(void *feature, int n)
cdef void gdal_flush_cache(void *cogr_ds)
cdef void* gdal_open_vector(char* path_c, int mode, drivers, options) except NULL
cdef void* gdal_create(void* cogr_driver, const char *path_c, options) except NULL
cdef OGRErr gdal_start_transaction(void *cogr_ds, int force)
cdef OGRErr gdal_commit_transaction(void *cogr_ds)
cdef OGRErr gdal_rollback_transaction(void *cogr_ds)
cdef OGRFieldSubType get_field_subtype(void *fielddefn)
cdef void set_field_subtype(void *fielddefn, OGRFieldSubType subtype)
cdef bint check_capability_create_layer(void *cogr_ds)

from fiona._shim cimport OGR_F_GetFieldAsInteger as OGR_F_GetFieldAsInteger64
from fiona._shim cimport OGR_F_SetFieldInteger as OGR_F_SetFieldInteger64
from fiona._shim cimport OGR_DS_GetLayerByName as GDALDatasetGetLayerByName
from fiona._shim cimport OGR_DS_GetLayer as GDALDatasetGetLayer
from fiona._shim cimport OGR_DS_Destroy as GDALClose
from fiona._shim cimport OGR_DS_GetDriver as GDALGetDatasetDriver
from fiona._shim cimport OGRGetDriverByName as GDALGetDriverByName
from fiona._shim cimport OGR_DS_GetLayerCount as GDALDatasetGetLayerCount
from fiona._shim cimport OGR_DS_DeleteLayer as GDALDatasetDeleteLayer
from fiona._shim cimport OGR_DS_CreateLayer as GDALDatasetCreateLayer
from fiona._shim cimport OGR_Dr_DeleteDataSource as GDALDeleteDataset
