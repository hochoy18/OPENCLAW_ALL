// StemCellNetwork.cs - 干细胞知识网络图
// USE CASE: 高中生物选择性必修3 干细胞知识点整理

using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;
using DocForge.Core;

namespace DocForge.Templates;

public static class StemCellNetwork
{
    private static readonly Themes.ColorSet Theme = Themes.Forest;

    // A4 dimensions in twips
    private const uint A4Width = 11906;
    private const uint A4Height = 16838;

    public static void Build(string outputPath, string assetDir)
    {
        using var doc = WordprocessingDocument.Create(outputPath, WordprocessingDocumentType.Document);
        var main = doc.AddMainDocumentPart();
        main.Document = new Document(new Body());
        var body = main.Document.Body!;

        // Create header/footer
        var (headerId, footerId) = CreateHeaderFooter(main);

        // Render cover
        RenderCover(body);
        EndSection(body, headerId, footerId, firstPageDifferent: true);

        // Render section 1: 基本概念
        RenderBasicConcepts(body);
        EndSection(body, headerId, footerId, firstPageDifferent: false);

        // Render section 2: ES细胞
        RenderESCells(body);
        EndSection(body, headerId, footerId, firstPageDifferent: false);

        // Render section 3: iPS细胞
        RenderIPSCells(body);
        EndSection(body, headerId, footerId, firstPageDifferent: false);

        // Render section 4: 三种干细胞比较
        RenderComparison(body);
        EndSection(body, headerId, footerId, firstPageDifferent: false);

        Fields.EnableAutoRefresh(main);
        main.Document.Save();
    }

    private static (string headerId, string footerId) CreateHeaderFooter(MainDocumentPart main)
    {
        // Header
        var headerPart = main.AddNewPart<HeaderPart>();
        headerPart.Header = new Header(
            new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Center }
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 9, Theme.Muted),
                    new Text("高中生物 · 干细胞")
                )
            )
        );
        headerPart.Header.Save();

        // Footer with page number
        var footerPart = main.AddNewPart<FooterPart>();
        footerPart.Footer = new Footer(
            new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Center }
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 9, Theme.Muted),
                    Fields.CurrentPage()
                )
            )
        );
        footerPart.Footer.Save();

        return (main.GetIdOfPart(headerPart), main.GetIdOfPart(footerPart));
    }

    private static void EndSection(Body body, string headerId, string footerId, bool firstPageDifferent)
    {
        var sectPr = new SectionProperties(
            new SectionType { Val = SectionMarkValues.NextPage },
            new PageSize { Width = A4Width, Height = A4Height },
            new PageMargin
            {
                Top = 1134,
                Right = 1134,
                Bottom = 1134,
                Left = 1134,
                Header = 720,
                Footer = 720
            },
            new HeaderReference { Type = HeaderFooterValues.Default, Id = headerId },
            new FooterReference { Type = HeaderFooterValues.Default, Id = footerId }
        );

        if (firstPageDifferent)
        {
            sectPr.Append(new TitlePage());
        }

        body.Append(new Paragraph(new ParagraphProperties(sectPr)));
    }

    private static void RenderCover(Body body)
    {
        body.Append(new Paragraph(new ParagraphProperties(Primitives.Gaps(100, 0))));

        // Main title
        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Center },
                Primitives.Gaps(0, 16)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 36, Theme.Heading, true),
                new Text("干细胞及其应用")
            )
        ));

        // Subtitle
        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Center },
                Primitives.Gaps(0, 40)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 16, Theme.Accent),
                new Text("知识网络图")
            )
        ));

        // Decorative line
        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Center },
                Primitives.Gaps(0, 60)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Muted),
                new Text("━━━━━━━━━━━━━━━━━━━━")
            )
        ));

        // Section overview
        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Center },
                Primitives.Gaps(0, 12)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Body),
                new Text("一、干细胞的基本概念")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Center },
                Primitives.Gaps(0, 12)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Body),
                new Text("二、胚胎干细胞（ES细胞）")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Center },
                Primitives.Gaps(0, 12)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Body),
                new Text("三、诱导多能干细胞（iPS细胞）")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Center },
                Primitives.Gaps(0, 12)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Body),
                new Text("四、三种干细胞的比较")
            )
        ));

        // Subject tag
        body.Append(new Paragraph(new ParagraphProperties(Primitives.Gaps(60, 0))));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Center }
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Muted),
                new Text("高中生物 · 选择性必修三 · 生物技术与工程")
            )
        ));
    }

    private static void RenderBasicConcepts(Body body)
    {
        AddPageBreak(body);

        // Section title
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 20)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 22, Theme.Heading, true),
                new Text("一、干细胞的基本概念")
            )
        ));

        // Definition
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【定义】")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Left },
                Primitives.Gaps(0, 12),
                Primitives.Margins(24, 0)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Body),
                new Text("干细胞是一类具有自我更新和分化潜能的细胞。")
            )
        ));

        // Classification
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【分类】")
            )
        ));

        var classifications = new[]
        {
            ("胚胎干细胞（ES细胞）", "来源于早期胚胎的囊胚内细胞团，具有全能性"),
            ("成体干细胞", "存在于成体各种组织中，具有多能性或单能性"),
            ("诱导多能干细胞（iPS细胞）", "通过重编程技术将体细胞诱导为多能性干细胞"),
        };

        foreach (var (title, desc) in classifications)
        {
            body.Append(new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Left },
                    Primitives.Gaps(10, 4)
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Accent, true),
                    new Text("◆ ")
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Heading, true),
                    new Text(title)
                )
            ));

            body.Append(new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Left },
                    Primitives.Gaps(0, 12),
                    Primitives.Margins(24, 0)
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 10, Theme.Body),
                    new Text(desc)
                )
            ));
        }
    }

    private static void RenderESCells(Body body)
    {
        AddPageBreak(body);

        // Section title
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 20)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 22, Theme.Heading, true),
                new Text("二、胚胎干细胞（ES细胞）")
            )
        ));

        // Discovery
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【首次成功获得】1981年")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Left },
                Primitives.Gaps(0, 12),
                Primitives.Margins(24, 0)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Body),
                new Text("科学家从体外培养的囊胚中成功分离并培养出胚胎干细胞")
            )
        ));

        // Source
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【来源】")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Left },
                Primitives.Gaps(0, 12),
                Primitives.Margins(24, 0)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Body),
                new Text("从囊胚的内细胞团中分离得到")
            )
        ));

        // Characteristics
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【主要特点】")
            )
        ));

        var features = new[]
        {
            ("自我更新能力", "能够长期培养并保持未分化状态"),
            ("多向分化潜能", "可以分化为机体几乎所有类型的细胞"),
        };

        foreach (var (title, desc) in features)
        {
            body.Append(new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Left },
                    Primitives.Gaps(8, 4)
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Accent, true),
                    new Text("【" + title + "】")
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Heading, true),
                    new Text(desc)
                )
            ));
        }

        // Applications
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【应用价值】")
            )
        ));

        var apps = new[]
        {
            "研究细胞分化机制",
            "药物筛选和毒理学研究",
            "组织工程和再生医学",
        };

        foreach (var app in apps)
        {
            body.Append(new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Left },
                    Primitives.Gaps(4, 4),
                    Primitives.Margins(24, 0)
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Body),
                    new Text("• " + app)
                )
            ));
        }
    }

    private static void RenderIPSCells(Body body)
    {
        AddPageBreak(body);

        // Section title
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 20)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 22, Theme.Heading, true),
                new Text("三、诱导多能干细胞（iPS细胞）")
            )
        ));

        // Discovery time
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【发现时间】2006年")
            )
        ));

        // Definition
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【概念】")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Left },
                Primitives.Gaps(0, 12),
                Primitives.Margins(24, 0)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Body),
                new Text("诱导多能干细胞（induced pluripotent stem cell），简称iPS细胞")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Left },
                Primitives.Gaps(0, 12),
                Primitives.Margins(24, 0)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 10, Theme.Muted),
                new Text("通过人工诱导，使已分化的体细胞重编程，恢复类似胚胎干细胞的多能性")
            )
        ));

        // Preparation methods
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【制备方法】")
            )
        ));

        var methods = new[]
        {
            ("��毒载体法", "将特定基因（Oct4、Sox2、Klf4、c-Myc等）导入细胞中"),
            ("蛋白直接导入法", "将重编程蛋白直接导入细胞中"),
            ("小分子化合物诱导法", "使用小分子化合物诱导细胞重编程"),
        };

        foreach (var (title, desc) in methods)
        {
            body.Append(new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Left },
                    Primitives.Gaps(8, 4)
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Heading, true),
                    new Text("• " + title + "：")
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Body),
                    new Text(desc)
                )
            ));
        }

        // Cell sources
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【细胞来源】")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Left },
                Primitives.Gaps(0, 12),
                Primitives.Margins(24, 0)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Body),
                new Text("最初从成纤维细胞转化而来，后来发现分化后的T细胞、B细胞等也可以被诱导为iPS细胞")
            )
        ));

        // Application prospects
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【应用前景】")
            )
        ));

        var prospects = new[]
        {
            ("细胞替代治疗", "神经细胞、心肌细胞、肝细胞、胰岛细胞、肠上皮细胞、血细胞"),
            ("组织修复", "用于移植修复受损组织和器官"),
            ("疾病模型", "建立疾病模型用于研究"),
            ("药物筛选", "用于新药开发和测试"),
        };

        foreach (var (title, desc) in prospects)
        {
            body.Append(new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Left },
                    Primitives.Gaps(10, 4)
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Heading, true),
                    new Text("• " + title + "：")
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 10, Theme.Body),
                    new Text(desc)
                )
            ));
        }
    }

    private static void RenderComparison(Body body)
    {
        AddPageBreak(body);

        // Section title
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 20)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 22, Theme.Heading, true),
                new Text("四、三种干细胞的比较")
            )
        ));

        // Comparison table header
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【对比表】")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Left },
                Primitives.Gaps(0, 12),
                Primitives.Margins(24, 0)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 10, Theme.Muted),
                new Text("类型                来源                分化潜能                应用特点")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Left },
                Primitives.Gaps(0, 8),
                Primitives.Margins(24, 0)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 10, Theme.Body),
                new Text("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            )
        ));

        var comparisons = new[]
        {
            ("胚胎干细胞", "囊胚内细胞团", "全能性/多能性", "分化能力强，但存在伦理问题"),
            ("成体干细胞", "各种成体组织", "多能性或单能性", "伦理问题少，但分化范围有限"),
            ("iPS细胞", "体细胞重编程", "多能性", "避免伦理争议，个性化医疗潜力大"),
        };

        foreach (var row in comparisons)
        {
            body.Append(new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Left },
                    Primitives.Gaps(0, 8),
                    Primitives.Margins(24, 0)
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 10, Theme.Heading, true),
                    new Text(row.Item1 + "          ")
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 10, Theme.Body),
                    new Text(row.Item2 + "     " + row.Item3 + "     " + row.Item4)
                )
            ));
        }

        // Summary
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 24)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("【总结】")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Left },
                Primitives.Gaps(0, 12),
                Primitives.Margins(24, 0)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Body),
                new Text("iPS细胞避免了胚胎干细胞的伦理争议，且能从患者自身细胞获取，具有个性化医疗的巨大潜力，是近年来干细胞研究的热点方向。")
            )
        ));
    }

    private static void AddPageBreak(Body body)
    {
        body.Append(new Paragraph(new Run(new Break { Type = BreakValues.Page })));
    }
}