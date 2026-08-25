# Foundation

The Foundation collection defines the philosophy, method, and editorial rules
used to develop the DunderCode Engineering System (DESys). It describes DESys
itself; it does not automatically become policy for a consumer repository.

Consumer projects may adopt Foundation guidance through their own approved
policies and decisions. When consumer evidence conflicts with vendored DESys
guidance, the consumer's code, runtime behavior, and approved documentation take
precedence.

## Components

The Foundation has three governed components:

| Component | Responsibility | Canonical document |
| --- | --- | --- |
| Canon | Engineering philosophy and enduring principles | [DEC-0001](canon/DEC-0001-engineering-manifesto.md) |
| Method | Iterative engineering method | [DEM-0001](../knowledge/dem/DEM-0001-engineering-method.md) |
| Documentation | Editorial and metadata rules | [DCSG-0001](documentation/DCSG-0001-canon-style-guide.md) |

The `glossary/` directory is reserved for future terminology assets. Its empty
files are not governed documents and are excluded from the public reference
corpus until substantive content is approved.

`style-guide/README.md` is a compatibility navigation surface. Editorial
ownership remains with the Documentation component and DCSG-0001.

## Relationship

```text
Engineering philosophy (DEC)
            |
            v
Engineering method (DEM)
            |
            v
Documentation rules (DCSG)
            |
            v
Standards and project adoption
```

This relationship provides traceability; it does not imply that every project
must follow one sequential process or adopt every DESys standard.

## Navigation

| Objective | Read |
| --- | --- |
| Understand DESys engineering principles | [Canon](canon/README.md) |
| Understand the iterative DESys method | [Method](method/README.md) |
| Write and review DESys documents | [Documentation](documentation/README.md) |
| Browse technical standards | [DES standards](../knowledge/des/README.md) |

## Maintenance

Changes to Foundation documents require canonical metadata validation, editorial
review, and explicit lifecycle approval. Generated indexes support discovery but
do not create authority or approval.
