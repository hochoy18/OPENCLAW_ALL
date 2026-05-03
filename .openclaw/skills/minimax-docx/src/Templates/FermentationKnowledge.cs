// FermentationKnowledge.cs - 发酵工程知识网络图
// USE CASE: 高中生物发酵工程知识点整理

using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;
using DocForge.Core;

namespace DocForge.Templates;

public static class FermentationKnowledge
{
    private static readonly Themes.ColorSet Theme = Themes.Ocean;

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

        // Render section 1: 基本环节
        RenderBasicSteps(body);
        EndSection(body, headerId, footerId, firstPageDifferent: false);

        // Render section 2: 特点
        RenderCharacteristics(body);
        EndSection(body, headerId, footerId, firstPageDifferent: false);

        // Render section 3: 应用
        RenderApplications(body);
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
                    new Text("高中生物 · 发酵工程")
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
                new Text("发酵工程及其应用")
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
                new Text("一、发酵工程的基本环节")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Center },
                Primitives.Gaps(0, 12)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Body),
                new Text("二、发酵工程的特点")
            )
        ));

        body.Append(new Paragraph(
            new ParagraphProperties(
                new Justification { Val = JustificationValues.Center },
                Primitives.Gaps(0, 12)
            ),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Body),
                new Text("三、发酵工程的应用")
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

    private static void RenderBasicSteps(Body body)
    {
        AddPageBreak(body);

        // Section title
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 20)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 22, Theme.Heading, true),
                new Text("一、发酵工程的基本环节")
            )
        ));

        // Process flow description
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 16)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Accent, true),
                new Text("中心环节：发酵罐内发酵")
            )
        ));

        // Process steps as a styled table
        var steps = new[]
        {
            ("1", "选育菌种", "目的：获得性状优良的菌种\n来源：自然筛选、诱变育种、基因工程"),
            ("2", "扩大培养", "将菌种数量扩增至一定规模"),
            ("3", "培养基的配制与灭菌", "配制适合菌种生长的培养基，并进行严格灭菌"),
            ("4", "接种", "将菌种接入无菌培养基"),
            ("5", "发酵罐内发酵", "严格控制温度、pH、氧气等条件（中心环节）"),
            ("6", "分离、提纯产物", "若产物是代谢物：分离提纯\n若产物是微生物本身：过滤或沉淀"),
            ("7", "获得产品", "得到最终发酵产品"),
        };

        foreach (var (num, title, desc) in steps)
        {
            // Step number circle effect using colored text
            body.Append(new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Left },
                    Primitives.Gaps(8, 4)
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 12, Theme.Accent, true),
                    new Text($"【{num}】")
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

    private static void RenderCharacteristics(Body body)
    {
        AddPageBreak(body);

        // Section title
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 20)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 22, Theme.Heading, true),
                new Text("二、发酵工程的特点")
            )
        ));

        var characteristics = new[]
        {
            ("产物专一", "发酵工程生产的产物具有高度特异性，即特定的微生物产生特定的代谢产物。"),
            ("生产条件温和", "一般在常温常压下进行，不需要高温高压等苛刻条件。"),
            ("原料丰富廉价", "可以利用农副产品、工业废水、废弃农作物等作为发酵原料。"),
            ("废弃物对环境污染小", "发酵工程的废弃物多为天然物质，可被生物降解，对环境友好。"),
        };

        foreach (var (title, desc) in characteristics)
        {
            // Bullet with accent color
            body.Append(new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Left },
                    Primitives.Gaps(10, 6)
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 14, Theme.Accent, true),
                    new Text("◆ ")
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 14, Theme.Heading, true),
                    new Text(title)
                )
            ));

            body.Append(new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Left },
                    Primitives.Gaps(0, 16),
                    Primitives.Margins(24, 0)
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Body),
                    new Text(desc)
                )
            ));
        }
    }

    private static void RenderApplications(Body body)
    {
        AddPageBreak(body);

        // Section title
        body.Append(new Paragraph(
            new ParagraphProperties(Primitives.Gaps(0, 20)),
            new Run(
                Primitives.TextStyle("Arial", "Microsoft YaHei", 22, Theme.Heading, true),
                new Text("三、发酵工程的应用")
            )
        ));

        // Application areas
        var applications = new[]
        {
            ("食品工业", new[] {
                "酱油生产：利用米曲霉发酵大豆制成",
                "柠檬酸：黑曲霉发酵淀粉类物质",
                "味精（谷氨酸）：谷氨酸棒状杆菌发酵",
                "酶制剂：淀粉酶、果胶酶、蛋白酶等"
            }),
            ("医药工业", new[] {
                "基因工程药物：胰岛素、干扰素、疫苗等",
                "抗生素：青霉素、链霉素等",
                "维生素：维生素C、维生素B12等"
            }),
            ("农牧业", new[] {
                "微生物肥料：根瘤菌肥、固氮菌肥",
                "微生物农药：苏云金杆菌（Bt）",
                "微生物饲料：单细胞蛋白（SCP）"
            }),
            ("其他方面", new[] {
                "能源生产：利用废料发酵产生酒精、乙烯",
                "洗涤剂：含酶洗衣粉",
                "环保：生物降解塑料、污水处理"
            }),
        };

        foreach (var (category, items) in applications)
        {
            // Category header with background effect
            body.Append(new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Left },
                    Primitives.Gaps(16, 8)
                ),
                new Run(
                    Primitives.TextStyle("Arial", "Microsoft YaHei", 14, Theme.Accent, true),
                    new Text($"【{category}】")
                )
            ));

            foreach (var item in items)
            {
                body.Append(new Paragraph(
                    new ParagraphProperties(
                        new Justification { Val = JustificationValues.Left },
                        Primitives.Gaps(4, 4),
                        Primitives.Margins(24, 0)
                    ),
                    new Run(
                        Primitives.TextStyle("Arial", "Microsoft YaHei", 11, Theme.Body),
                        new Text($"• {item}")
                    )
                ));
            }
        }
    }

    private static void AddPageBreak(Body body)
    {
        body.Append(new Paragraph(new Run(new Break { Type = BreakValues.Page })));
    }
}
